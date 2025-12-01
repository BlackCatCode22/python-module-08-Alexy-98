# chat_bot_demo_code.py
import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load environment variables from .env
load_dotenv()
# The fix: os.getenv() retrieves the value of the environment variable named "OPENAI_API_KEY"
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY is not set. "
        "Create an .env file with OPENAI_API_KEY=your_secret_key_here"
    )

# 2. Create OpenAI client
client = OpenAI(api_key=api_key)

# 3. Streamlit page config
st.set_page_config(page_title="CIT-95 Chatbot Demo", page_icon="🤖")
st.title("🤖 CIT-95 Python Chatbot Demo")
st.write(
    "Ask any question about Python, CIT-95 assignments, or general programming.\n\n"
    "_This demo uses GPT-4-class models via the OpenAI Chat Completions API._"
)

# 4. Initialize conversation state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a friendly Python tutor for a college programming class (CIT-95). "
                "Explain concepts clearly and use beginner-friendly examples."
            ),
        }
    ]

# 5. Display chat messages (ignore system message)
for msg in st.session_state.messages[1:]:
    role = "👤 Student" if msg["role"] == "user" else "🤖 Tutor"
    st.markdown(f"**{role}:** {msg['content']}")

st.write("---")

# 6. User input box
user_input = st.text_area(
    "Type your question here:",
    placeholder="Example: What does a Python list do?",
)

col1, col2 = st.columns(2)
with col1:
    send_clicked = st.button("Ask the bot")
with col2:
    clear_clicked = st.button("Clear conversation")

# 7. Clear chat
if clear_clicked:
    st.session_state.messages = st.session_state.messages[:1]  # keep only system prompt
    st.rerun()  # NEW Streamlit-safe version

# 8. Handle question submission
if send_clicked and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=st.session_state.messages,
            temperature=0.7,
            max_tokens=500,
        )

        assistant_reply = completion.choices[0].message.content

        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_reply}
        )

        st.rerun()  # NEW Streamlit-safe refresh

    except Exception as e:
        st.error(f"Error talking to OpenAI API: {e}")