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
        response = client.chat.completions.create(  # ✅ Updated OpenAI API
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant that knows everything about Qiyu Hu, a UX & AI designer."},
                {"role": "user", "content": user_input}
            ]
        )
        answer = response.choices[0].message.content  # ✅ Corrected response format
        st.write(f"AI: {answer}")
    else:
        st.write("Please enter a question!")

