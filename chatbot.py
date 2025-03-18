import openai
import streamlit as st
import os
from dotenv import load_dotenv

# ✅ Load API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("❌ API key not found! Make sure it's set in the `.env` file.")
    st.stop()

# ✅ Create OpenAI Client
client = openai.OpenAI(api_key=api_key)

# ✅ System Prompt for AI Behavior
system_prompt = """
You are **Qiyu Hu’s severed innie**, an AI-driven extension of her knowledge.
You respond in a **concise, engaging, and structured way**.
- **Before user input, suggest 3 engaging conversation starters**.
- **After every response, provide 3 relevant follow-up questions**.
- Follow-ups should feel **natural and connected** to the current topic.

Now, answer concisely and suggest 3 related follow-up questions.
"""

# ✅ Streamlit UI
st.title("Chat with Qiyu Hu’s AI Assistant 🤖")
st.write("Ask me anything about Qiyu’s experience, projects, and design philosophy!")

# ✅ Initial Conversation Starters
default_questions = [
    "Who is Qiyu Hu and what makes her design approach unique?",
    "What are some of Qiyu's most innovative AI projects?",
    "How does Qiyu see the future of AI and UX design?"
]

# ✅ Initialize session state for follow-ups
if "follow_up_questions" not in st.session_state:
    st.session_state.follow_up_questions = []
if "full_answer" not in st.session_state:
    st.session_state.full_answer = ""
if "show_full_response" not in st.session_state:
    st.session_state.show_full_response = False
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# ✅ Display Initial Conversation Starters
if not st.session_state.user_input:
    st.write("🔹 **Not sure what to ask? Try one of these:**")
    for question in default_questions:
        if st.button(question):
            st.session_state.user_input = question
            st.rerun()  # Immediately trigger response

# ✅ User Input Field
user_input = st.text_input("You: ", st.session_state.user_input)

# ✅ AI Response Logic with Follow-Up Suggestions
if st.button("Ask AI") or st.session_state.user_input:
    if st.session_state.user_input:
        with st.spinner("AI is thinking..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": st.session_state.user_input}
                ],
                max_tokens=300  
            )

            full_answer = response.choices[0].message.content

            # ✅ Split response into main answer + follow-ups
            if "Follow-up questions:" in full_answer:
                main_response, follow_ups = full_answer.split("Follow-up questions:")
            else:
                main_response, follow_ups = full_answer, ""

            # ✅ Store full response
            st.session_state.full_answer = main_response.strip()

            # ✅ Display AI Answer
            st.write(f"**AI:** {st.session_state.full_answer}")

            # ✅ Extract Follow-Up Suggestions
            follow_up_list = [q.strip("- ") for q in follow_ups.strip().split("\n") if q.strip()]
            st.session_state.follow_up_questions = follow_up_list[:3]  # Limit to 3 suggestions

        # ✅ Reset user input after AI response
        st.session_state.user_input = ""

# ✅ Show Follow-Up Questions
if st.session_state.follow_up_questions:
    st.write("🔍 **Keep the Conversation Going:**")
    for question in st.session_state.follow_up_questions:
        if st.button(question):
            st.session_state.user_input = question  # Set follow-up as the next user query
            st.rerun()  # Immediately re-trigger response
