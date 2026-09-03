import os

import streamlit as st
from dotenv import load_dotenv
from google import genai


# --------------------------------
# Load environment variables
# --------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY not found in .env")
    st.stop()


# --------------------------------
# Gemini client
# --------------------------------

client = genai.Client(api_key=api_key)


# --------------------------------
# Page configuration
# --------------------------------

st.set_page_config(
    page_title="Helper AI",
    page_icon="🤖",
    layout="centered"
)


# --------------------------------
# Custom CSS
# --------------------------------

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background: linear-gradient(
            135deg,
            #0f172a,
            #1e293b,
            #111827
        );
        color: white;
    }

    /* Title */
    h1 {
        color: #60a5fa;
        text-align: center;
    }

    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #cbd5e1;
        margin-bottom: 30px;
    }

    /* User message */
    [data-testid="stChatMessage"] {
        border-radius: 15px;
        padding: 10px;
    }

    /* Chat input */
    [data-testid="stChatInput"] {
        border-radius: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------
# Header
# --------------------------------

st.title("🤖 Helper AI Chatbot")

st.markdown(
    '<div class="subtitle">'
    'powered by gtec kuthuparamba'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------
# Initialize chat history
# --------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------
# Display chat history
# --------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --------------------------------
# Chat input
# --------------------------------

user_input = st.chat_input(
    "Ask Helper AI something..."
)


# --------------------------------
# Generate response
# --------------------------------

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

    try:

        # Send message to Gemini
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
