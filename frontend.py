import streamlit as st
import requests
import json

BACKEND_URL = "http://localhost:8000"

# Page config
st.set_page_config(
    page_title="InvestBuddy - Your Investment Assistant",
    page_icon="💰",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .disclaimer-box {
        background-color: #E9D5FF;
        border-left: 4px solid #9333EA;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        color: #1F2937;
    }
    .form-container {
        background-color: #F8FAFC;
        padding: 2rem;
        border-radius: 1rem;
        border: 1px solid #E2E8F0;
        margin: 1rem 0;
    }
    .etf-card {
        background-color: #F8FAFC;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border: 1px solid #E2E8F0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "awaiting_response" not in st.session_state:
    st.session_state.awaiting_response = False

if "user_profile_completed" not in st.session_state:
    st.session_state.user_profile_completed = False

if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}

# Title
st.markdown('<div class="main-header">💰 InvestBuddy</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Your Personal Investment Assistant for Beginners</div>', unsafe_allow_html=True)

# Disclaimer - Always visible at the top
st.markdown("""
<div class="disclaimer-box">
    <h4>⚠️ Important Disclaimer</h4>
    <p><strong>Please read carefully before using InvestBuddy:</strong></p>
    <ul>
        <li>InvestBuddy provides <strong>educational information only</strong> and is not professional financial advice.</li>
        <li><strong>All investments carry risk</strong> and you may lose some or all of your invested capital.</li>
        <li>Past performance does not guarantee future results.</li>
        <li>We do <strong>not take any responsibility</strong> for any financial losses or risks you may incur.</li>
        <li>Before making any investment decisions, consult with a licensed financial advisor.</li>
        <li>Only invest money you can afford to lose and understand the risks involved.</li>
    </ul>
    <p style="margin-top: 1rem;"><em>By using InvestBuddy, you acknowledge that you understand and accept these terms.</em></p>
</div>
""", unsafe_allow_html=True)

# Show onboarding form if profile not completed
if not st.session_state.user_profile_completed:
    st.markdown("### 📋 Tell Us About Yourself")
    st.markdown("Please fill out this quick form so we can provide you with personalized investment guidance.")

    with st.form("user_profile_form"):
        st.markdown('<div class="form-container">', unsafe_allow_html=True)

        # Basic Information
        st.subheader("💼 Basic Information")
        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("Your Age", min_value=18, max_value=100, value=30, step=1)
            monthly_income = st.number_input("Monthly Income (AZN)", min_value=0.0, value=0.0, step=100.0,
                                             help="Your total monthly income before expenses")

        with col2:
            marital_status = st.selectbox("Marital Status", ["Single", "Married", "Other"])
            has_kids = st.selectbox("Do you have children?", ["No", "Yes"])

        # Children details (only if they have kids)
        kids_count = 0
        kids_ages = []
        if has_kids == "Yes":
            col1, col2 = st.columns(2)
            with col1:
                kids_count = st.number_input("Number of Children", min_value=1, max_value=10, value=1, step=1)
            with col2:
                kids_ages_input = st.text_input("Ages of Children (comma-separated)",
                                                placeholder="e.g., 5, 8, 12",
                                                help="Enter ages separated by commas")
                if kids_ages_input:
                    try:
                        kids_ages = [int(age.strip()) for age in kids_ages_input.split(",")]
                    except:
                        st.warning("Please enter valid ages separated by commas")

        st.markdown("---")

        # Financial Information
        st.subheader("💰 Financial Situation")
        col1, col2 = st.columns(2)

        with col1:
            current_savings = st.number_input("Current Savings (AZN)", min_value=0.0, value=0.0, step=500.0,
                                              help="How much money do you have saved?")
            monthly_expenses = st.number_input("Monthly Expenses (AZN)", min_value=0.0, value=0.0, step=100.0,
                                               help="Include food, utilities, transportation, etc.")

        with col2:
            monthly_rent = st.number_input("Monthly Rent/Mortgage (AZN)", min_value=0.0, value=0.0, step=100.0,
                                           help="Leave as 0 if you own your home outright")
            existing_debt = st.number_input("Total Debt (AZN)", min_value=0.0, value=0.0, step=500.0,
                                            help="Include all loans, credit cards, etc.")

        st.markdown("---")

        # Investment Goals
        st.subheader("🎯 Investment Goals")

        primary_goal = st.selectbox(
            "What is your primary investment goal?",
            [
                "Building long-term wealth",
                "Saving for retirement",
                "Buying a house",
                "Children's education",
                "Starting a business",
                "Emergency fund",
                "Short-term savings (1-3 years)",
                "Other"
            ]
        )

        if primary_goal == "Other":
            other_goal = st.text_input("Please specify your goal:")
            if other_goal:
                primary_goal = other_goal

        time_horizon = st.selectbox(
            "When do you need this money?",
            [
                "Less than 1 year",
                "1-3 years",
                "3-5 years",
                "5-10 years",
                "10+ years",
                "No specific timeline"
            ]
        )

        risk_tolerance = st.select_slider(
            "How comfortable are you with investment risk?",
            options=["Very Conservative", "Conservative", "Moderate", "Aggressive", "Very Aggressive"],
            value="Moderate",
            help="Higher risk can mean higher returns, but also higher losses"
        )

        st.markdown("---")

        # Additional Information
        st.subheader("📝 Additional Information (Optional)")
        additional_info = st.text_area(
            "Anything else you'd like us to know?",
            placeholder="e.g., planning to get married soon, expecting a salary increase, other financial obligations...",
            height=100
        )

        st.markdown('</div>', unsafe_allow_html=True)

        # Terms acceptance
        accept_terms = st.checkbox(
            "I have read and understood the disclaimer above and accept that InvestBuddy does not provide professional financial advice.",
            value=False
        )

        # Submit button
        submitted = st.form_submit_button("Continue to Chat 💬", type="primary", use_container_width=True)

        if submitted:
            if not accept_terms:
                st.error("❌ Please accept the disclaimer to continue.")
            elif monthly_income <= 0:
                st.error("❌ Please enter your monthly income.")
            else:
                # Store user profile
                st.session_state.user_profile = {
                    "age": age,
                    "monthly_income": monthly_income,
                    "marital_status": marital_status,
                    "has_kids": has_kids,
                    "kids_count": kids_count if has_kids == "Yes" else 0,
                    "kids_ages": kids_ages if has_kids == "Yes" else [],
                    "current_savings": current_savings,
                    "monthly_expenses": monthly_expenses,
                    "monthly_rent": monthly_rent,
                    "existing_debt": existing_debt,
                    "primary_goal": primary_goal,
                    "time_horizon": time_horizon,
                    "risk_tolerance": risk_tolerance,
                    "additional_info": additional_info
                }

                st.session_state.user_profile_completed = True

                # Create initial system message with user profile
                profile_summary = f"""
User Profile:
- Age: {age} years old
- Monthly Income: {monthly_income:,.2f} AZN
- Marital Status: {marital_status}
- Children: {kids_count} (ages: {', '.join(map(str, kids_ages)) if kids_ages else 'N/A'})
- Current Savings: {current_savings:,.2f} AZN
- Monthly Expenses: {monthly_expenses:,.2f} AZN (including {monthly_rent:,.2f} AZN rent/mortgage)
- Total Debt: {existing_debt:,.2f} AZN
- Primary Goal: {primary_goal}
- Time Horizon: {time_horizon}
- Risk Tolerance: {risk_tolerance}
{f"- Additional Context: {additional_info}" if additional_info else ""}
"""

                # Add welcome message
                welcome_msg = f"""👋 **Welcome to InvestBuddy!**

Thank you for sharing your information. Based on your profile:
- You're {age} years old and earn {monthly_income:,.2f} AZN monthly
- Your primary goal is: **{primary_goal}**
- Time horizon: **{time_horizon}**

I'm here to help you create a personalized investment plan. Feel free to ask me anything about:
- Whether you're ready to start investing
- What investments suit your situation
- How much you should invest monthly
- Step-by-step guides on how to invest

What would you like to know first? 😊
"""

                st.session_state.messages.append({
                    "role": "system",
                    "content": profile_summary
                })

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": welcome_msg
                })

                st.rerun()

else:
    # Show user profile summary in sidebar
    with st.sidebar:
        st.header("👤 Your Profile")
        profile = st.session_state.user_profile

        st.metric("Age", f"{profile['age']} years")
        st.metric("Monthly Income", f"{profile['monthly_income']:,.0f} AZN")
        st.metric("Savings", f"{profile['current_savings']:,.0f} AZN")

        if st.button("🔄 Update Profile", use_container_width=True):
            st.session_state.user_profile_completed = False
            st.session_state.messages = []
            st.rerun()

        st.markdown("---")

        # Live ETF Prices
        st.header("📊 Popular ETFs")

        try:
            etfs_response = requests.get(f"{BACKEND_URL}/etfs/recommended", timeout=5)
            if etfs_response.status_code == 200:
                etfs = etfs_response.json()["data"]
                for symbol, data in etfs.items():
                    st.markdown(f"**{symbol}**")
                    st.caption(data['name'])
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.metric(label="Price", value=f"${data['price']:.2f}")
                    with col2:
                        st.metric(label="Change", value=data['change_percent'])
                    st.markdown("---")
            else:
                st.info("ETF prices unavailable")
        except Exception as e:
            st.info("Loading ETF prices...")

        st.markdown("---")

        # System Status
        st.header("⚙️ System Status")

        try:
            health = requests.get(f"{BACKEND_URL}/health", timeout=2)
            if health.status_code == 200:
                st.success("✅ Connected")
            else:
                st.error("❌ Error")
        except:
            st.error("❌ Offline")

        st.markdown("---")

        if st.button("🗑️ Clear Chat History", use_container_width=True):
            # Keep system message with profile, clear the rest
            system_messages = [msg for msg in st.session_state.messages if msg["role"] == "system"]
            st.session_state.messages = system_messages
            st.rerun()

    # Display chat history
    for msg in st.session_state.messages:
        if msg["role"] != "system":  # Don't display system messages
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Handle quick question responses
    if st.session_state.awaiting_response and len(st.session_state.messages) > 0:
        last_msg = st.session_state.messages[-1]
        if last_msg["role"] == "user":
            # Get backend response
            with st.chat_message("assistant"):
                with st.spinner("💭 Analyzing your situation..."):
                    try:
                        response = requests.post(
                            f"{BACKEND_URL}/chat",
                            json={
                                "messages": st.session_state.messages,
                                "model": "gpt-3.5-turbo"
                            },
                            timeout=30
                        )

                        if response.status_code == 200:
                            bot_msg = response.json()["message"]
                            st.markdown(bot_msg)

                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": bot_msg
                            })
                        else:
                            st.error(f"Error {response.status_code}: {response.text}")

                    except requests.exceptions.ConnectionError:
                        st.error("❌ Backend not reachable at http://localhost:8000")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")

            # Reset the flag
            st.session_state.awaiting_response = False
            st.rerun()

    # Chat Input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        # Get backend response
        with st.chat_message("assistant"):
            with st.spinner("💭 Analyzing your situation..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/chat",
                        json={
                            "messages": st.session_state.messages,
                            "model": "gpt-3.5-turbo"
                        },
                        timeout=30
                    )

                    if response.status_code == 200:
                        bot_msg = response.json()["message"]
                        st.markdown(bot_msg)

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": bot_msg
                        })
                    else:
                        st.error(f"Error {response.status_code}: {response.text}")

                except requests.exceptions.ConnectionError:
                    st.error("❌ Backend not reachable at http://localhost:8000")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

        st.rerun()