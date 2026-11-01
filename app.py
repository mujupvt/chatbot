import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Mitra AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# 2. GEMINI CONNECTION
# ==================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY is not configured.")
    st.stop()

client = genai.Client(api_key=api_key)

# ==================================================
# 3. SESSION STATE
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

# ==================================================
# 4. PREMIUM CSS
# ==================================================

st.markdown("""
<style>

/* Main background */

.stApp {
    background:
        radial-gradient(ellipse at top left,
        #25204b 0%, transparent 40%),
        linear-gradient(135deg,
        #080d1b, #111827, #15152b);
    color: #f8fafc;
}

/* Main container */

.block-container {
    max-width: 1050px;
    padding-top: 35px;
    padding-bottom: 100px;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: #0c1222;
    border-right: 1px solid #27304a;
}

/* Main title */

.mitra-logo {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    letter-spacing: -1px;
    background: linear-gradient(
        90deg, #8b7cff, #54c8ff
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 5px;
}

/* Subtitle */

.mitra-subtitle {
    text-align: center;
    color: #9ca9c2;
    font-size: 15px;
    margin-bottom: 35px;
}

/* Welcome title */

.welcome-title {
    font-size: 32px;
    font-weight: 750;
    text-align: center;
    color: #ffffff;
    margin-top: 60px;
}

.welcome-description {
    text-align: center;
    color: #a3adc2;
    font-size: 15px;
    margin-bottom: 30px;
}

/* Chat messages */

[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 17px;
    margin-bottom: 15px;
}

/* Message text */

[data-testid="stChatMessage"] p {
    color: #e8edf8;
    line-height: 1.7;
    font-size: 15px;
}

/* Input area */

[data-testid="stChatInput"] > div {
    background: #1b2235 !important;
    border: 1px solid #5147a8 !important;
    border-radius: 18px !important;
}

/* Input text */

[data-testid="stChatInput"] textarea {
    color: white !important;
}

/* Buttons */

.stButton button {
    background: linear-gradient(
        100deg, #635bff, #895cf6
    );
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px;
    transition: 0.25s;
}

/* Button hover */

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 20px #635bff50;
    border: none;
}

/* Sidebar text */

section[data-testid="stSidebar"] p {
    color: #cbd5e1;
}

/* Divider */

hr {
    border-color: #29324a;
}

/* Mobile */

@media(max-width: 600px) {

    .block-container {
        padding: 20px 15px 90px;
    }

    .mitra-logo {
        font-size: 34px;
    }

    .welcome-title {
        font-size: 25px;
        margin-top: 35px;
    }

    [data-testid="stChatMessage"] {
        padding: 12px;
    }
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# 5. SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown("## 🤖 Mitra AI")

    st.caption("Your AI companion")

    st.divider()

    if st.button("＋  New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.rerun()

    st.markdown("### Your Assistant")

    st.markdown("""
    - 💬 AI conversations
    - 🧠 Gemini intelligence
    - ⚡ Quick answers
    """)

    st.divider()

    st.markdown("### About")

    st.write("Created by *Mujthaba*")

    st.caption("Data Science Student")
    st.caption("GTEC Kuthuparamba")

    st.divider()

    st.caption("Powered by Google Gemini")

    st.caption("Mitra AI © 2026")

# ==================================================
# 6. MAIN HEADER
# ==================================================

st.markdown(
    '<div class="mitra-logo">✦ Mitra AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="mitra-subtitle">'
    'Your intelligent AI companion · Ask anything'
    '</div>',
    unsafe_allow_html=True
)

# ==================================================
# 7. WELCOME SCREEN
# ==================================================

if not st.session_state.messages:

    st.markdown(
        '<div class="welcome-title">'
        'Hello! What can I help you with? 👋'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="welcome-description">'
        'Ask questions, explore ideas and learn something new.'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "💻  Learn Programming",
            use_container_width=True
        ):
            st.session_state.pending_prompt = (
                "Teach me Python programming from beginner level."
            )

    with col2:

        if st.button(
            "📊  Data Science",
            use_container_width=True
        ):
            st.session_state.pending_prompt = (
                "Explain Data Science in simple language."
            )

    col3, col4 = st.columns(2)

    with col3:

        if st.button(
            "💡  Generate Ideas",
            use_container_width=True
        ):
            st.session_state.pending_prompt = (
                "Give me some creative project ideas."
            )

    with col4:

        if st.button(
            "🌍  Ask Anything",
            use_container_width=True
        ):
            st.session_state.pending_prompt = (
                "What are some interesting things I can learn today?"
            )

# ==================================================
# 8. DISPLAY CHAT HISTORY
# ==================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ==================================================
# 9. CHAT INPUT
# ==================================================

user_input = st.chat_input(
    "Message Mitra AI..."
)

if st.session_state.pending_prompt:

    user_input = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

# ==================================================
# 10. GEMINI RESPONSE
# ==================================================

if user_input:

    # Display user message

    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Build conversation context

    conversation = []

    for message in st.session_state.messages:

        conversation.append({
            "role": (
                "user" if message["role"] == "user"
                else "model"
            ),
            "parts": [
                {"text": message["content"]}
            ]
        })

    # Generate response

    try:

        with st.chat_message("assistant"):

            with st.spinner("Mitra AI is thinking..."):

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=conversation
                )

                reply = response.text

                if not reply:
                    reply = "Sorry, I couldn't generate a response."

            st.markdown(reply)

        st.session_state.messages.append({
            "role": "assistant",
            "content": reply
        })

    except Exception as e:

        error_message = f"Something went wrong: {e}"

        with st.chat_message("assistant"):
            st.error(error_message)

        st.session_state.messages.append({
            "role": "assistant",
            "content": error_message
        })
