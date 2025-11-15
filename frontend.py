import streamlit as st
import requests

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
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .example-question {
        background-color: #F1F5F9;
        padding: 0.75rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 3px solid #3B82F6;
        cursor: pointer;
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

# Title
st.markdown('<div class="main-header">💰 InvestBuddy</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Your Personal Investment Assistant for Beginners</div>', unsafe_allow_html=True)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Track if we need to get a response (for quick questions)
if "awaiting_response" not in st.session_state:
    st.session_state.awaiting_response = False

# Show welcome message and quick start questions if no messages yet
if len(st.session_state.messages) == 0:
    st.info("👋 **Welcome to InvestBuddy!** I'm here to help you start your investment journey. "
            "I'll ask you some simple questions about your finances and goals, then create a personalized "
            "investment plan just for you. Ready to begin?")

    # Quick Start Questions Menu
    st.markdown("### 💡 Quick Start Questions")
    st.markdown("Click any question below to get started:")

    # Define quick start questions
    quick_questions = [
        "How should I start investing?",
        "How do I actually buy stocks? (step-by-step)",
        "What's the difference between stocks and bonds?",
        "What's an ETF and why should I use it?",
        "I want a safe investment - what do you recommend?",
        "Where can I invest? (show me platforms)",
    ]

    # Create buttons for each question
    cols = st.columns(2)
    for idx, question in enumerate(quick_questions):
        col = cols[idx % 2]
        with col:
            if st.button(f"❓ {question}", key=f"quick_q_{idx}", use_container_width=True):
                # Add user message
                st.session_state.messages.append({"role": "user", "content": question})
                st.session_state.awaiting_response = True
                st.rerun()

    st.markdown("---")

# Display chat history
for msg in st.session_state.messages:
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

# Sidebar
with st.sidebar:
    # Live ETF Prices
    st.header("📊 Popular ETFs")

    try:
        etfs_response = requests.get(f"{BACKEND_URL}/etfs/recommended", timeout=5)
        if etfs_response.status_code == 200:
            etfs = etfs_response.json()["data"]
            for symbol, data in etfs.items():
                # Determine color for change
                change_color = "🟢" if "-" not in data['change_percent'] else "🔴"

                # Display each ETF
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
        st.session_state.messages = []
        st.rerun()