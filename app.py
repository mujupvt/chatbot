```python
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai

# ==========================================================
# 1. PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Mitra AI",
    page_icon="🤖",
    layout="centered",
)

# ==========================================================
# 2. LOAD ENVIRONMENT VARIABLES
# ==========================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY is not configured. Please check your .env file.")
    st.stop()

# ==========================================================
# 3. GEMINI CLIENT
# ==========================================================

client = genai.Client(api_key=api_key)

# ==========================================================
# 4. CUSTOM CSS
# ==========================================================

st.markdown(
    """
    <style>
    /* Main page */
    .stApp {
        background: linear-gradient(
            180deg,
            #1a2639 0%,
            #172338 55%,
            #111925 100%
        );
        color: white;
    }

    /* Main content width */
    .block-container {
        max-width: 760px;
        padding-top: 30px;
        padding-bottom: 130px;
    }

    /* Header */
    .mitra-title {
        text-align: center;
        font-size: 38px;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 25px;
    }

    .created-text {
        text-align: center;
        font-size: 15px;
        color: #d5dce7;
        margin-bottom: 15px;
    }

    .creator-name {
        text-align: center;
        font-size: 40px;
        font-weight: 700;
        color: #dce4ef;
        margin-bottom: 45px;
    }

    .student-text {
        text-align: center;
        font-size: 25px;
        font-weight: 600;
        color: #dce4ef;
        margin-bottom: 35px;
    }

    /* Chat messages */
    [data-testid="stChatMessage"] {
        border-radius: 12px;
        padding: 10px 12px;
        margin-bottom: 14px;
    }

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) {
        background: #202733;
    }

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) {
        background: transparent;
    }

    [data-testid="stChatMessage"] p {
        color: #f1f5f9;
        font-size: 15px;
        line-height: 1.6;
    }

    /* Chat input */
    [data-testid="stChatInput"] > div {
        background: #272831;
        border: 1px solid #ff3943;
        border-radius: 10px;
        box-shadow: none;
    }

    [data-testid="stChatInput"] textarea {
        background: transparent !important;
        color: white !important;
        font-size: 14px !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #a7a9b3 !important;
        opacity: 1;
    }

    [data-testid="stChatInput"] > div:focus-within {
        border-color: #ff3943;
        box-shadow: 0 0 0 1px #ff3943;
    }

    [data-testid="stChatInput"] button {
        background: #454752 !important;
        border-radius: 8px;
        color: white !important;
    }

    [data-testid="stChatInput"] button:hover {
        background: #5a5c68 !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 7px;
    }

    ::-webkit-scrollbar-track {
        background: #111722;
    }

    ::-webkit-scrollbar-thumb {
        background: #394355;
        border-radius: 10px;
    }

    /* Mobile responsive */
    @media (max-width: 600px) {
        .block-container {
            padding-left: 15px;
            padding-right: 15px;
            padding-top: 20px;
        }

        .mitra-title {
            font-size: 30px;
        }

        .created-text {
            font-size: 14px;
        }

        .creator-name {
            font-size: 32px;
            margin-bottom: 30px;
        }

        .student-text {
            font-size: 20px;
            margin-bottom: 25px;
        }

        [data-testid="stChatMessage"] {
            padding: 8px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================================
# 5. HEADER
# ==========================================================

st.markdown(
    """
    <div class="mitra-title">🤖 Mitra AI</div>

    <div class="created-text">Created by</div>

    <div class="creator-name">Mujthaba</div>

    <div class="student-text">
        Data Science Student<br>
        GTEC Kuthuparamba
    </div>
    """,
    unsafe_allow_html=True,
)

# ==========================================================
# 6. INITIALIZE CHAT HISTORY
# ==========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================================
# 7. DISPLAY OLD MESSAGES
# ==========================================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================================
# 8. CHAT INPUT
# ==========================================================

user_input = st.chat_input("Ask Mitra AI something...")

# ==========================================================
# 9. HANDLE USER MESSAGE
# ==========================================================

if user_input:
    # Display and save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate Gemini response
    with st.chat_message("assistant"):
        with st.spinner("Mitra AI is thinking..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=user_input,
                )

                reply = response.text

                if not reply:
                    reply = "Sorry, I couldn't generate a response. Please try again."

            except Exception:
                reply = (
                    "Sorry, something went wrong while connecting to Gemini. "
                    "Please check your API key, internet connection, and model access."
                )

        st.markdown(reply)

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reply,
        }
    )
```
