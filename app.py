import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="Italiano AI Tutor", page_icon="🇮🇹")

# Sidebar for Settings
with st.sidebar:
    st.title("Settings")
    api_key = st.text_input("Enter Google API Key", type="password")
    level = st.selectbox("Student Level", ["A1 (Beginner)", "A2 (Elementary)", "B1 (Intermediate)"])
    response_lang = st.radio("Explain in:", ["English", "Italian"])
    
    st.divider()
    
    if st.button("Generate Quiz"):
        st.session_state.trigger_quiz = True
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.trigger_quiz = False
        st.rerun()

# Check for API Key
if not api_key:
    st.warning("Please enter your API Key in the sidebar to start.")
    st.stop()

# Configure AI
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []
if "trigger_quiz" not in st.session_state:
    st.session_state.trigger_quiz = False

# System Instructions
system_instruction = f"""
You are an expert Italian Language Tutor.
Student Level: {level}
Explanation Language: {response_lang}

RULES:
1. Speak primarily in {response_lang}.
2. Keep vocabulary appropriate for {level}.
3. Gently correct mistakes with explanations.
4. If asked for a quiz, provide 5 questions and WAIT for answers.
"""

# Display Chat History
st.title("Italiano AI Tutor")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle Quiz Trigger
if st.session_state.trigger_quiz:
    user_prompt = "Please generate a 5-question vocabulary quiz suitable for my level. Do not show answers yet."
    st.session_state.trigger_quiz = False
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)
    
    with st.chat_message("assistant"):
        try:
            full_context = f"{system_instruction}\n\nUser: {user_prompt}"
            response = model.generate_content(full_context)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
    st.rerun()

# Handle User Input
if prompt := st.chat_input("Ask a question or practice Italian..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            full_context = f"{system_instruction}\n\nUser: {prompt}"
            response = model.generate_content(full_context)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")