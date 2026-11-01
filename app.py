import os
import streamlit as st
from google import genai

# Page configuration
st.set_page_config(
    page_title="Mitra AI",
    page_icon="🤖",
    layout="centered",
)

# Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY is missing. Add it in Render Environment.")
    st.stop()

# Gemini client
client = genai.Client(api_key=api_key)

# Custom CSS
css = """
<style>
.stApp {
    background: linear-gradient(180deg, #1a2639, #172338, #111925);
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
    color: #d5dce7;
    font-size: 15px;
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
    font-size: 23px;
    font-weight: 600;
    line-height: 1.6;
    color: #dce4ef;
    margin-bottom: 35px;
}

[data-testid="stChatMessage"] {
    border-radius: 12px;
    padding: 10px;
    margin-bottom: 12px;
}

[data-testid="stChatInput"] > div {
    background: #272831;
    border: 1px solid #ff3943;
    border-radius: 10px;
}

[data-testid="stChatInput"] textarea {
    color: white !important;
}

@media (max-width: 600px) {
    .block-container {
        padding-left: 15px;
        padding-right: 15px;
    }

    .mitra-title {
        font-size: 30px;
    }

    .creator-name {
        font-size: 32px;
    }

    .student-text {
        font-size: 19px;
    }
}
</style>
"""

st.markdown(css, unsafe_allow_html=True)

# Header
st.markdown(
    '<div class="mitra-title">🤖 Mitra AI</div>'
    '<div class="created-text">Created by</div>'
    '<div class="creator-name">Mujthaba</div>'
    '<div class="student-text">'
    'Data Science Student<br>GTEC Kuthuparamba'
    '</div>',
    unsafe_allow_html=True,
)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Ask Mitra AI something...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Mitra AI is thinking..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=user_input,
                )

                reply = response.text or "Please try again."

            except Exception as error:
                print(f"Gemini API error: {error}")
                reply = (
                    "Sorry, an error occurred. Please check your "
                    "Gemini API key and model access."
                )

        st.markdown(reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
