import streamlit as st
import os
from openai import OpenAI
from services.database_manager import DatabaseManager
from models.it_ticket import ITTicket 


st.set_page_config(page_title="AI assistant", page_icon="🤖 ",
layout="wide")
# Ensure state keys exist (in case user opens this page first)
if "users" not in st.session_state:
 st.session_state.logged_in = False
if "username" not in st.session_state:
 st.session_state.username = ""
# Guard: if not logged in, send user back
if not st.session_state.logged_in:
 st.error("You must be logged in to view the dashboard.")
 if st.button("Go to login page"):
   st.switch_page("Home.py") # back to the first page
 st.stop()

 st.title("IT operations Dashboard")
st.success(f"Hello, **{st.session_state.username}**! You are logged in.")
# Example dashboard layout
st.caption("This is an AI Assistant for general use")



#	Initialize	OpenAI	client 
client = OpenAI(api_key	= st.secrets["OPENAI_API_KEY"] )

	 
#	Page	title 
st.title("AI Assistant") 
	 
#	Initialize	session	state	for	messages 
if 'messages' not in st.session_state: 
    st.session_state.messages = [ 
        { 
		 "role": "system", 
		 "content": """You	are	an	AI 	assistant."""
        }
    ]        
	             
	 
#	Display	all	previous	messages 
for	message	in	st.session_state.messages: 
	if	message["role"]	!=	"system":		#	Don't	display	system	prompt
		with	st.chat_message(message["role"]): 
			st.markdown(message["content"]) 
	 
#	Get	user	input 
prompt	= st.chat_input("Ask about any questions...") 
	 
if prompt:
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to session state
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Call OpenAI API with streaming
    with st.spinner("Thinking..."):
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=st.session_state.messages,
            stream=True
        )

   # Display streaming response
    with st.chat_message("assistant"):
        container = st.empty()
        full_reply = ""

    for chunk in completion:
        delta = chunk.choices[0].delta
        if delta.content:
            full_reply += delta.content
            container.markdown(full_reply + "▌")  # Typing cursor effect

    # Remove cursor and show final response
    container.markdown(full_reply)

# Save assistant response
    st.session_state.messages.append({
          "role": "assistant",
          "content": full_reply
   })
    
