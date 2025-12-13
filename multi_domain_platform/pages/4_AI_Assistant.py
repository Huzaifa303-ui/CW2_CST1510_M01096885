import streamlit as st
from openai import OpenAI
import time
from services.ai_assistant import AIAssistant
st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")

st.title("This is an AI Assistant. Ask me anything!")
# Login guard
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to login page"):
        st.switch_page("Home.py")
    st.stop()

st.success(f"Hello, **{st.session_state.username}**! You are logged in.")
st.caption("This is an AI Assistant for general use")

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize AI assistant object in session state
if "ai_assistant" not in st.session_state:
    st.session_state.ai_assistant = AIAssistant()

# Display previous messages
for msg in st.session_state.ai_assistant._history:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Chat input
prompt = st.chat_input("Ask any question...")
if prompt:
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI reply
    with st.spinner("Thinking..."):
        reply = st.session_state.ai_assistant.send_message(prompt, client)

    # Display assistant response letter by letter
    with st.chat_message("assistant"):
        placeholder = st.empty()
        typed_text = ""

    for char in reply:
        typed_text += char
        placeholder.markdown(typed_text + "▌")  # cursor effect
        time.sleep(0.005)  # adjust typing speed here


    placeholder.markdown(typed_text)  # remove cursor

    


# Clear chat button
if st.button("Clear Chat"):
    st.session_state.ai_assistant.clear_history()
    st.rerun()
    
