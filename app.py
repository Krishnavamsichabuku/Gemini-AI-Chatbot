import streamlit as st
import google.generativeai as genai
from streamlit_chat import message

# Set up the API key
api_key = "AIzaSyDTlK29XOLzhy5uQlSQ_wunPaBsNRuyTGQ"
genai.configure(api_key=api_key)

# Streamlit UI Setup
st.set_page_config(page_title="Google Gemini Chatbot", page_icon="🤖", layout="centered")

# Inject external HTML and CSS (Assuming these files exist)
with open("templates/style.css") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

with open("templates/index.html") as html_file:
    st.markdown(html_file.read(), unsafe_allow_html=True)

# Function to generate responses based on chat history
def generate_response(prompt, chat_history):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        chat = model.start_chat(history=chat_history)
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        return "⚠️ Sorry, I couldn't process your request. Please try again later!"

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if 'bot_history' not in st.session_state:
    st.session_state['bot_history'] = []

# Input Section
user_input = st.text_input(
    "💬 Type your message here:",
    placeholder="What’s on your mind? Ask me anything!",
    key="input"
)

# Ask me again button
ask_again_button = st.button("Ask me again")

# Process user input and generate a response
if user_input.strip() or ask_again_button:
    if ask_again_button:
        # Clear chat history if "Ask me again" button is clicked
        st.session_state['chat_history'] = []
        st.session_state['bot_history'] = []
        user_input = ""  # Reset user input field

    if user_input.strip():
        with st.spinner("🤔 Thinking..."):
            response = generate_response(user_input, st.session_state['chat_history'])

        # Update chat history
        st.session_state['chat_history'].append(user_input)
        st.session_state['bot_history'].append(response)

# Display chat history
if st.session_state['chat_history']:
    for i in range(len(st.session_state['chat_history'])):
        message(st.session_state['chat_history'][i], is_user=True, key=f"user_{i}")
        message(st.session_state['bot_history'][i], key=f"bot_{i}")
