import os

import streamlit as st
from dotenv import load_dotenv
from google import genai


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY is not configured.")
    st.stop()


# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(api_key=api_key)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Mitra AI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* ==============================
       GLOBAL
    ============================== */

    * {
        box-sizing: border-box;
    }

    html, body, [class*="css"] {
        font-family: Arial, sans-serif;
    }

    .stApp {
        background:
            linear-gradient(
                180deg,
                #1a2639 0%,
                #172338 55%,
                #111925 100%
            );

        color: #ffffff;
    }


    /* Remove Streamlit default top space */

    .block-container {
        max-width: 760px;
        padding-top: 25px;
        padding-bottom: 130px;
    }


    /* ==============================
       HEADER
    ============================== */

    .mitra-header {
        text-align: center;
        padding-top: 5px;
        padding-bottom: 25px;
    }


    .mitra-title {
        font-size: 38px;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 25px;
        letter-spacing: -1px;
    }


    .created-text {
        font-size: 15px;
        color: #d5dce7;
        margin-bottom: 18px;
    }


    .creator-name {
        font-size: 38px;
        font-weight: 700;
        color: #dce4ef;
        margin-bottom: 55px;
    }


    .student-text {
        font-size: 30px;
        font-weight: 600;
        color: #dce4ef;
        margin-bottom: 55px;
    }


    .college-text {
        font-size: 30px;
        font-weight: 600;
        color: #dce4ef;
        margin-bottom: 35px;
    }


    /* ==============================
       CHAT AREA
    ============================== */

    [data-testid="stChatMessage"] {
        border-radius: 12px;
        padding: 10px 12px;
        margin-bottom: 15px;
    }


    /* User message */

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) {
        background: #202733;
    }


    /* Message text */

    [data-testid="stChatMessage"] p {
        color: #f1f5f9;
        font-size: 15px;
    }


    /* ==============================
       CHAT AVATAR
    ============================== */

    [data-testid="stChatMessageAvatar"] {
        border-radius: 8px;
    }


    /* ==============================
       CHAT INPUT
    ============================== */

    [data-testid="stChatInput"] {
        background: #0d1017;
        border-top: 1px solid #0d1017;
        padding: 15px 0 25px 0;
    }


    [data-testid="stChatInput"] > div {
        background: #272831;
        border: 1px solid #ff3943;
        border-radius: 8px;
        box-shadow: none;
    }


    [data-testid="stChatInput"] textarea {
        background: transparent !important;
        color: #ffffff !important;
        font-size: 14px !important;
    }


    [data-testid="stChatInput"] textarea::placeholder {
        color: #a7a9b3 !important;
        opacity: 1;
    }


    /* Input focus */

    [data-testid="stChatInput"] > div:focus-within {
        border-color: #ff3943;
        box-shadow: 0 0 0 1px #ff3943;
    }


    /* ==============================
       SEND BUTTON
    ============================== */

    [data-testid="stChatInput"] button {
        background: #454752 !important;
        border-radius: 8px;
    }


    [data-testid="stChatInput"] button:hover {
        background: #555866 !important;
    }


    /* ==============================
       SCROLLBAR
    ============================== */

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


    /* ==============================
       MOBILE
    ============================== */

    @media (max-width: 600px) {

        .block-container {
            padding-left: 15px;
            padding-right: 15px;
            padding-top: 20px;
        }


        .mitra-title {
            font-size: 30px;
        }


        .creator-name {
            font-size: 32px;
            margin-bottom: 40px;
        }


        .student-text {
            font-size: 23px;
            margin-bottom: 40px;
        }


        .college-text {
            font-size: 22px;
            margin-bottom: 30px;
        }


        [data-testid="stChatMessage"] {
            padding: 8px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="mitra-header">

        <div class="mitra-title">
            🤖 Mitra AI
        </div>

        <div class="created-text">
            Created by
        </div>

        <div class="creator-name">
            Mujthaba
        </div>

        <div class="student-text">
            Data Science Student
        </div>

        <div class="college-text">
            GTEC Kuthuparamba
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# INITIALIZE CHAT HISTORY
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# =========================================================
# CHAT INPUT
# =========================================================

user_input = st.chat_input(
    "Ask Helper AI something..."
)


# =========================================================
# GENERATE RESPONSE
# =========================================================

if user_input:

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )


    # Gemini response
    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=user_input
        )

        reply = response.text


    except Exception as e:

        reply = f"Error: {e}"


    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(reply)


    # Save AI response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reply
        }
    )
