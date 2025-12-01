# chat_bot_merged.py

import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# ---------------------------------------
# 1. Load environment variables
# ---------------------------------------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY is not set.\n"
        "Create a .env file with:\n\nOPENAI_API_KEY=your_key_here"
    )

# ---------------------------------------
# 2. OpenAI Client
# ---------------------------------------
client = OpenAI(api_key=api_key)

# ---------------------------------------
# 3. Helper Functions
# ---------------------------------------
def sanitize_response(response: str) -> str:
    """
    Cleans unwanted filler phrases or duplicate text.
    Extend this if needed.
    """
    cleaned = response.replace("", "")
    cleaned = cleaned.replace("Ah, yes", "")
    return cleaned.strip()

# ---------------------------------------
# 4. Streamlit Page Setup
# ---------------------------------------
st.set_page_config(page_title="AI Tutor Chatbot", page_icon="🤖")

st.title("🤖 AI Tutor Chatbot")

st.write(
    "This chatbot supports multiple personalities and remembers the conversation.\n"
    "Ask any question about Python, classes, homework, or programming!"
)

# ---------------------------------------
# 5. Personalities (Unified)
# ---------------------------------------
personalities = {
    "Friendly Tutor": (
        "You are a warm, encouraging tutor who explains things clearly."
    ),
    "Strict Professor": (
        "You are a strict professor who gives concise, academic explanations."
    ),
    "Sarcastic Secretary": (
        "You are a sarcastic yet helpful administrator with razor sharp wit."
    ),
    "Funny Mentor": (
        "You crack jokes while still giving helpful educational answers."
    ),
}

selected_personality = st.selectbox(
    "Choose a personality:",
    options=list(personalities.keys())
)

# ---------------------------------------
# 6. Initialize Chat
# ---------------------------------------
if (
    "personality" not in st.session_state
    or st.session_state.personality != selected_personality
):
    st.session_state.personality = selected_personality
    st.session_state.messages = [
        {"role": "system", "content": personalities[selected_personality]}
    ]

# ---------------------------------------
# 7. Display Chat History
# ---------------------------------------
for msg in st.session_state.messages[1:]:
    role = "👤 Student" if msg["role"] == "user" else "🤖 Tutor"
    st.markdown(f"**{role}:** {msg['content']}")

st.write("---")

# ---------------------------------------
# 8. Clear Chat Button
# ---------------------------------------
if st.button("Clear conversation"):
    st.session_state.messages = [
        {"role": "system", "content": personalities[selected_personality]}
    ]
    st.rerun()

# ---------------------------------------
# 9. Chat Input (Enter to send)
# ---------------------------------------
user_input = st.chat_input("Type your question here:")

if user_input:
    # Add user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    # Query OpenAI
    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=st.session_state.messages,
            temperature=0.7,
            max_tokens=500,
        )

        raw_reply = completion.choices[0].message.content
        clean_reply = sanitize_response(raw_reply)

        # Add assistant message
        st.session_state.messages.append(
            {"role": "assistant", "content": clean_reply}
        )

        st.rerun()

    except Exception as e:
        st.error(f"Error communicating with OpenAI API:\n{e}")

# ---------------------------------------
# 10. Optional Console Test Mode
# ---------------------------------------
def main():
    test_prompt = "Tell me about turtles."
    print("Test mode:", sanitize_response(test_prompt))

if __name__ == "__main__":
    if os.environ.get("STREAMLIT_RUN") != "true":
        main()
