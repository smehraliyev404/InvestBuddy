from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from typing import List, Optional
from dotenv import load_dotenv
import os
import uuid

# Import InvestBuddy modules
from database import init_database, save_message, get_conversation_history, create_or_get_user
from financial_api import get_stock_price, get_recommended_etfs
from investment_logic import generate_investment_recommendation
from prompts import INVESTMENT_ADVISOR_PROMPT
from vector_store import get_ai_context
from investment_platforms import get_all_platforms_for_ai, BEGINNERS_GUIDE

# Load .env variables
load_dotenv()

# Initialize database
init_database()

app = FastAPI()

print("🔑 Checking API Key...")
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print(f"✅ API Key loaded: {api_key[:8]}...{api_key[-4:]}")
else:
    print("❌ API Key NOT found in environment!")

# CORS settings for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
client = OpenAI(api_key=api_key)


# Request/Response Models
class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]
    model: str = "gpt-3.5-turbo"


class ChatResponse(BaseModel):
    message: str
    role: str = "assistant"


@app.get("/")
def read_root():
    return {
        "message": "InvestBuddy API is running!",
        "description": "AI-powered investment assistant for beginners",
        "version": "1.0.0"
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Convert Pydantic messages to dict format
        user_messages = [{"role": m.role, "content": m.content} for m in request.messages]

        # Extract user profile if it exists (should be first system message from frontend)
        user_profile = ""
        conversation_messages = []

        for msg in user_messages:
            if msg["role"] == "system" and "User Profile:" in msg["content"]:
                # This is the user profile from the form - store it separately
                user_profile = msg["content"]
            elif msg["role"] != "system":
                # Keep user and assistant messages for conversation history
                conversation_messages.append(msg)

        # Get the last user message for RAG context
        last_user_message = None
        for msg in reversed(conversation_messages):
            if msg["role"] == "user":
                last_user_message = msg["content"]
                break

        # Start building the enhanced system prompt
        enhanced_system_prompt = INVESTMENT_ADVISOR_PROMPT

        # Add user profile if available (right after main prompt for context)
        if user_profile:
            enhanced_system_prompt += f"""

---
**ABOUT THIS USER:**

{user_profile}

**Important:** Use this profile information to personalize your advice. Consider their age, income, family situation, goals, and risk tolerance when making recommendations.
---
"""

        # Always include platform information and practical guides
        platforms_info = get_all_platforms_for_ai()
        practical_guide = BEGINNERS_GUIDE

        enhanced_system_prompt += f"""

---
**INVESTMENT PLATFORMS** (Always mention these with links when user asks how to invest):

{platforms_info}

---
**PRACTICAL INVESTING GUIDE** (Use this to explain step-by-step how to invest):

{practical_guide}

---
"""

        # Get relevant ETF knowledge using RAG (with live data!)
        if last_user_message:
            etf_context = get_ai_context(last_user_message, n_results=3, include_live_data=True)

            if etf_context:
                enhanced_system_prompt += f"""
**RELEVANT ETF KNOWLEDGE WITH LIVE DATA** (Use this to provide better, more detailed answers):

{etf_context}

---
"""

        # Add final reminders
        enhanced_system_prompt += """
**CRITICAL REMINDERS:**
- Always explain in SIMPLE language (like talking to a friend who knows nothing about investing)
- When recommending investments, ALWAYS include:
  1. What to buy (e.g., "SPY - an ETF containing America's top 500 companies")
  2. WHY to buy it (with beginner explanation)
  3. CURRENT PRICE and performance (use the live data above if available)
  4. HOW to buy it (step-by-step using the platform guides above)
  5. Links to platforms where they can invest
- Never assume the user knows anything - explain everything!
- Use the user's profile information to give personalized advice
- Be conversational, friendly, and encouraging
---
"""

        # Construct final messages: system prompt + conversation history
        messages = [{"role": "system", "content": enhanced_system_prompt}] + conversation_messages

        # Debug: Print message structure
        print(f"\n🔍 Debug - Messages sent to AI:")
        print(f"   System prompt length: {len(enhanced_system_prompt)} chars")
        print(f"   Conversation messages: {len(conversation_messages)}")
        if last_user_message:
            print(f"   Last user message: {last_user_message[:100]}...")
        print()

        # Call OpenAI API
        response = client.chat.completions.create(
            model=request.model,
            messages=messages,
            temperature=0.7
        )

        bot_message = response.choices[0].message.content
        return ChatResponse(message=bot_message)

    except Exception as e:
        print(f"❌ Chat error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Simple webhook endpoint for n8n integration
class SimpleMessageRequest(BaseModel):
    message: str
    model: str = "gpt-3.5-turbo"


@app.post("/webhook/chat")
async def webhook_chat(request: SimpleMessageRequest):
    try:
        # Add system prompt for webhook too
        messages = [
            {"role": "system", "content": INVESTMENT_ADVISOR_PROMPT},
            {"role": "user", "content": request.message}
        ]

        response = client.chat.completions.create(
            model=request.model,
            messages=messages,
            temperature=0.7
        )

        bot_message = response.choices[0].message.content
        return {"response": bot_message, "success": True}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# New endpoints for InvestBuddy features

# Get stock/ETF price
@app.get("/stock/{symbol}")
async def get_stock(symbol: str):
    """Get current price for a stock or ETF symbol"""
    try:
        price_data = get_stock_price(symbol.upper())
        if price_data:
            return {
                "success": True,
                "data": price_data
            }
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Could not fetch price data for {symbol}"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get recommended ETFs with prices
@app.get("/etfs/recommended")
async def get_etfs():
    """Get list of recommended ETFs with current prices"""
    try:
        etfs = get_recommended_etfs()
        return {
            "success": True,
            "data": etfs,
            "count": len(etfs)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Generate investment recommendation
class InvestmentRequest(BaseModel):
    salary: float
    savings: float
    monthly_expenses: float
    debt: float = 0
    monthly_investment: float
    goal: str
    time_horizon_years: int


@app.post("/investment/recommend")
async def recommend_investment(request: InvestmentRequest):
    """Generate personalized investment recommendation"""
    try:
        recommendation = generate_investment_recommendation(
            salary=request.salary,
            savings=request.savings,
            monthly_expenses=request.monthly_expenses,
            debt=request.debt,
            monthly_investment=request.monthly_investment,
            goal=request.goal,
            time_horizon_years=request.time_horizon_years
        )

        return {
            "success": True,
            "data": recommendation
        }
    except Exception as e:
        print(f"❌ Recommendation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))