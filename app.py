import os

import streamlit as st
from dotenv import load_dotenv
from google import genai

# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Mitra AI",
    page_icon="🤖",
    layout="centered",
)

# ============================================================
# 2. LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY is not configured.")
    st.info("Please add GEMINI_API_KEY in your Render environment variables.")
    st.stop()

# ============================================================
# 3. GEMINI CLIENT
# ============================================================

client = genai.Client(api_key=api_key)

# ============================================================
# 4. CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(
            180deg,
            #1a2639 0%,
            #172338 55%,
            #111925 100%
        );
        color: white;
    }

    .block-container {
        max-width: 760px;
        padding-top: 30px;
        padding-bottom: 130px;
    }

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
        margin-bottom: 40px;
    }

    .student-text {
        text-align: center;
        font-size: 25px;
        font-weight: 600;
        line-height: 1.5;
        color: #dce4ef;
        margin-bottom: 35px;
    }

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

    @media (max-width: 600px) {
        .block-container {
            padding-left: 15px;
            padding-right: 15px;
            padding-top: 20px;
