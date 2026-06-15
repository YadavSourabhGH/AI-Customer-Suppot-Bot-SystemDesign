import streamlit as st
from bot_logic import SupportBot
import os
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(page_title="AI Customer Support Bot", page_icon="🤖")

st.title("🤖 AI Customer Support Bot")
st.markdown("Welcome! How can we help you today?")

# Initialize Groq API Key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if "bot" not in st.session_state:
    st.session_state.bot = SupportBot(api_key=GROQ_API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask your question..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response_placeholder = st.empty()
            response_text = ""

            for chunk in st.session_state.bot.stream_response(prompt, st.session_state.messages[:-1]):
                response_text += chunk
                response_placeholder.markdown(response_text)

            st.session_state.messages.append({"role": "assistant", "content": response_text})
