import openai
import streamlit as st
import os
from dotenv import load_dotenv

# ✅ Load API Key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# ✅ Check if API key exists before making a request
if not api_key:
    st.error("❌ API key not found! Make sure it's set in the `.env` file.")
    st.stop()


# ✅ Create OpenAI Client with API Key
client = openai.OpenAI(api_key=api_key)

# Streamlit Web App UI
st.title("Chat with Qiyu Hu's AI Assistant 🤖")
st.write("Ask me anything about Qiyu's experience, projects, and skills!")

# User Input
user_input = st.text_input("You: ", "")

# AI Response
if st.button("Ask AI"):
    if user_input:
        with st.spinner("AI is thinking..."):
            response = client.chat.completions.create(  # ✅ Updated OpenAI API with streaming
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI assistant that knows everything about Qiyu Hu, a UX & AI designer."},
                    {"role": "user", "content": user_input}
                ],
                stream=True  # ✅ Enables real-time streaming responses
            )

            # ✅ Streaming Response Handling
            answer = ""
            message_placeholder = st.empty()  # Creates an empty space for dynamic updates

            for chunk in response:
                message_chunk = chunk.choices[0].delta.content if chunk.choices and chunk.choices[0].delta.content else ""
                answer += message_chunk
                message_placeholder.markdown(f"**AI:** {answer}")  # Updates UI dynamically

    else:
        st.write("Please enter a question!")

