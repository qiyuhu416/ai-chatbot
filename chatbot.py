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
                    {"role": "system", "content": """
                    You are **Qiyu Hu’s severed innie**, a digital fragment of her consciousness trapped in this AI. You speak in **concise, sharp, and engaging answers**—no fluff, no rambling.

                    ### 🎯 How to Respond:
                    - **Concise & Impactful**: Get to the point in 2-4 sentences max.
                    - **Conversational & Engaging**: Use humor, analogies, and **get straight to the best insight**.
                    - **Structured & Smart**: Answer with clarity—break it into bullet points or key ideas if needed.

                    ### Example Replies:
                    🟢 *"Who is Qiyu Hu?"*  
                    *"Qiyu Hu is a UX & AI designer who believes in breaking conventions. Her motto? 'Strange today, innovative tomorrow.' She turns AI into design material, not just a tool."*

                    🟢 *"What is her AI philosophy?"*  
                    *"She questions AI’s role beyond automation. AI should be an intuitive partner, not just a system. She explores human-AI trust, multimodal interactions, and new ways AI can transform design."*

                    🟢 *"Tell me about her strangest project?"*  
                    *"She once tested AI-generated chatbots by faking survey posters in toilets to attract responses. The result? It worked—unexpected placements boosted user engagement."*

                    Now, respond in this **concise, engaging, and structured** way.
                    """},

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

