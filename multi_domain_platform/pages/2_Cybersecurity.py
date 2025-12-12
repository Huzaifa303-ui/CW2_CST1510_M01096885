import streamlit as st
import os
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from openai import OpenAI
from services.database_manager import DatabaseManager
from models.security_incident import SecurityIncident


st.set_page_config(page_title="Cybersecurity", page_icon="🛡️ ",
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

 st.title("Cybersecurity Dashboard")
st.success(f"Hello, **{st.session_state.username}**! You are logged in.")
# Example dashboard layout
st.caption("This is an AI for cybersecurity dashboard and incident management")





BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # pages folder
ROOT_DIR = os.path.dirname(BASE_DIR)  # project root

db_path = os.path.join(ROOT_DIR, "database", "platform.db")

db = DatabaseManager(db_path)
db.connect()
# Fetch data
rows = db.fetch_all(
    "SELECT id, title, severity, status, date FROM security_incidents"
)

# Convert rows into SecurityIncident objects
incidents: list[SecurityIncident] = []
for row in rows:
    incident = SecurityIncident(
        id=row[0],
        title=row[1],
        severity=row[2],
        status=row[3],
        date=row[4],
    )
    incidents.append(incident)


df = pd.DataFrame([{
    "id": inc.get_id(),
    "title": inc.get_title(),
    "severity": inc.get_severity(),
    "status": inc.get_status(),
    "date": inc.get_date()
} for inc in incidents])

df["date"] = pd.to_datetime(df["date"], errors="coerce")


graph_type = st.selectbox(
    "Choose graph type:",
    [
        "Bar Chart — Severity",
        "Pie Chart — Severity Breakdown",
        "Area Chart — Daily Trend"
    ]
)

if graph_type == "Bar Chart — Severity":
    counts = df["severity"].value_counts()

    fig, ax = plt.subplots()
    ax.bar(counts.index, counts.values)
    ax.set_title("Incident Severity Distribution")
    ax.set_xlabel("Severity")
    ax.set_ylabel("Count")
    st.pyplot(fig)

elif graph_type == "Pie Chart — Severity Breakdown":
    counts = df["severity"].value_counts()

    fig, ax = plt.subplots()
    ax.pie(counts.values, labels=counts.index, autopct="%1.1f%%")
    ax.set_title("Severity Breakdown")
    st.pyplot(fig)

elif graph_type == "Area Chart — Daily Trend":
    daily = df.groupby(df["date"].dt.date).size().reset_index(name="count")

    chart = px.area(daily, x="date", y="count", title="Daily Incident Trend")
    st.plotly_chart(chart)

#Streamlit UI

st.title("Cybersecurity Incidents")

for incident in incidents:
    with st.expander(f"Incident #{incident.get_id()} — {incident.get_title()}"):
        st.write(f"Severity: {incident.get_severity()}")
        st.write(f"Status: {incident.get_status()}")
        st.write(f"Date: {incident.get_date()}")

#	Initialize	OpenAI	client 
client = OpenAI(api_key	= st.secrets["OPENAI_API_KEY"] )

	 
#	Page	title 
st.title(" Cybersecurity AI Assistant") 
	 
#	Initialize	session	state	for	messages 
if 'messages' not in st.session_state: 
    st.session_state.messages = [ 
        { 
		 "role": "system", 
		 "content": """You	are	a	cybersecurity	expert	assistant. 
		 -	Analyze	incidents	and	threats 
		 -	Provide	technical	guidance 
		 -	Explain	attack	vectors	and	mitigations 
	     -	Use	standard	terminology	(MITRE	ATT&CK,	CVE) 
		 -	Prioritize	actionable	recommendations 
		 Tone:	Professional,	technical 
		 Format:	Clear,	structured	responses""" 
        }
    ]        
	             
	 
#	Display	all	previous	messages 
for	message	in	st.session_state.messages: 
	if	message["role"]	!=	"system":		#	Don't	display	system	prompt
		with	st.chat_message(message["role"]): 
			st.markdown(message["content"]) 
	 
#	Get	user	input 
prompt	= st.chat_input("Ask about cybersecurity...") 
	 
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
    
