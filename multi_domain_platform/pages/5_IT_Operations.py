import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from openai import OpenAI
from services.database_manager import DatabaseManager
from models.it_ticket import ITTicket 


st.set_page_config(page_title="IT operations", page_icon="🛠️ ",
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
st.caption("This is an AI for IT operations dashboard and incident management")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # pages folder
ROOT_DIR = os.path.dirname(BASE_DIR)  # project root

db_path = os.path.join(ROOT_DIR, "database", "platform.db")

db = DatabaseManager(db_path)
db.connect()


st.subheader("+ Create New Ticket")

with st.form("create_ticket_form"):
    title = st.text_input("Ticket Title")
    priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
    status = st.selectbox("Status", ["Open", "Investigating", "Resolved", "Mitigated","Closed"])
    created_date = st.date_input("Date")

    submitted = st.form_submit_button("Create Ticket")

    if submitted:
        db.create_ITticket( title, priority, status, created_date)
        st.success("Ticket created successfully.")
        st.rerun()



# Fetch data
rows = db.fetch_all(
    "SELECT id, title, priority, status, created_date FROM it_tickets"
)

# Convert rows into SecurityIncident objects
incidents: list[ITTicket] = []
for row in rows:
    incident = ITTicket(
        id=row[0],
        title=row[1],
        priority=row[2],
        status=row[3],
        created_date=row[4],
    )
    incidents.append(incident)

st.subheader(" IT Tickets")

for incident in incidents:
    with st.expander(f"Incident #{incident.get_id()} — {incident.get_title()}"):

        # Editable fields
        new_priority = st.selectbox(
            "Priority",
            ["Low", "Medium", "High", "Critical"],
            index=["Low", "Medium", "High", "Critical"].index(incident.get_priority()),
            key=f"prio_{incident.get_id()}"
        )

        new_status = st.selectbox(
            "Status",
            ["Open", "Investigating", "Resolved", "Mitigated","Closed"],
            index=["Open", "Investigating", "Resolved", "Mitigated","Closed"].index(incident.get_status()),
            key=f"status_{incident.get_id()}"
        )

        # Update button
        if st.button("Update", key=f"update_{incident.get_id()}"):
            db.update_ITticket(
                incident.get_id(),
                new_priority,
                new_status
            )
            st.success("Incident updated.")
            st.rerun()

        # Delete button
        if st.button("🗑 Delete", key=f"delete_{incident.get_id()}"):
            db.delete_ITticket(incident.get_id())
            st.warning("Incident deleted.")
            st.rerun()




df = pd.DataFrame([{
    "id": ticket.get_id(),
    "title": ticket.get_title(),
    "priority": ticket.get_priority(),
    "status": ticket.get_status(),
    "created_date": pd.to_datetime(ticket.get_created_date())
} for ticket in incidents])

# Graph Selection
graph_type = st.selectbox(
    "Select Graph Type:",
    ["Bar Chart — Priority Counts", "Pie Chart — Status Breakdown", "Line Chart — Tickets Over Time"]
)


# Graph Display
if graph_type == "Bar Chart — Priority Counts":
    counts = df["priority"].value_counts()
    fig, ax = plt.subplots()
    ax.bar(counts.index, counts.values, color="lightcoral")
    ax.set_title("Tickets per Priority")
    ax.set_xlabel("Priority")
    ax.set_ylabel("Count")
    st.pyplot(fig)

elif graph_type == "Pie Chart — Status Breakdown":
    counts = df["status"].value_counts()
    fig, ax = plt.subplots()
    ax.pie(counts.values, labels=counts.index, autopct="%1.1f%%", startangle=90)
    ax.set_title("Tickets by Status")
    st.pyplot(fig)

elif graph_type == "Line Chart — Tickets Over Time":
    # Count tickets per day
    daily_counts = df.groupby(df["created_date"].dt.date).size().reset_index(name="count")
    chart = px.line(daily_counts, x="created_date", y="count", markers=True,
                    title="Tickets Over Time", labels={"created_date":"Date", "count":"Number of Tickets"})
    st.plotly_chart(chart)

#Streamlit UI


#	Initialize	OpenAI	client 
client = OpenAI(api_key	= st.secrets["OPENAI_API_KEY"] )

	 
#	Page	title 
st.title(" IT operations AI Assistant") 
	 
#	Initialize	session	state	for	messages 
if 'messages' not in st.session_state: 
    st.session_state.messages = [ 
        { 
		 "role": "system", 
		 "content": """You	are	an	IT operations	assistant.
         1. Provide	helpful	and	accurate	information	related	to	IT	operations	and	incident	management.
         2. Answer	questions	about	best	practices,	tools,	and	techniques	used	in	IT	operations.
         3. Assist	users	in	troubleshooting	common	IT	issues	and	provide	guidance	on	resolving	incidents.
         4. Keep	your	responses	clear,	concise,	and	user-friendly.
        5. Use	a	professional	and	polite	tone	when	interacting	with	users."""
        }
    ]        
	             
	 
#	Display	all	previous	messages 
for	message	in	st.session_state.messages: 
	if	message["role"]	!=	"system":		#	Don't	display	system	prompt
		with	st.chat_message(message["role"]): 
			st.markdown(message["content"]) 
	 
#	Get	user	input 
prompt	= st.chat_input("Ask about IT operations...") 
	 
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
    
