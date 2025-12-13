import streamlit as st
import os
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from openai import OpenAI
from services.database_manager import DatabaseManager
from models.dataset import Dataset 


st.set_page_config(page_title="Data Science", page_icon="📊 ",
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

 st.title("Data Science Dashboard")
st.success(f"Hello, **{st.session_state.username}**! You are logged in.")
# Example dashboard layout
st.caption("This is an AI for Data Science dashboard and incident management")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # pages folder
ROOT_DIR = os.path.dirname(BASE_DIR)  # project root

db_path = os.path.join(ROOT_DIR, "database", "platform.db")

db = DatabaseManager(db_path)
db.connect()


st.subheader("+ Create New Incident")

with st.form("create_incident_form"):
    title = st.text_input("Incident Title")
    severity = st.text_input("Source")
    status = st.selectbox("Category", ["Business", "Health", "Finance", "Education", "Environment","Security","IT", "Other"])
    date = st.number_input("Size")

    submitted = st.form_submit_button("Create Incident")

    if submitted:
        db.create_dataset_incident(title, severity, status, date)
        st.success("Incident created successfully.")
        st.rerun()


# Fetch data
rows = db.fetch_all(
    "SELECT id, name, source, category, size FROM datasets_metadata"
)

# Convert rows into DatasetIncident objects
incidents: list[Dataset] = []
for row in rows:
    incident = Dataset(
        id=row[0],
        name=row[1],
        source=row[2],
        category=row[3],
        size=row[4],
    )
    incidents.append(incident)

st.subheader(" Dataset Incidents")

for incident in incidents:
    with st.expander(f"Incident #{incident.get_id()} — {incident.get_name()}"):

        # Editable fields
        new_source = st.text_input(
            "Source",
            value=incident.get_source(),
            key=f"source_{incident.get_id()}"
        )

        new_category = st.selectbox(
            "Category",
            ["Business", "Health", "Finance", "Education", "Environment", "Security", "IT", "Other"],
            index=["Business", "Health", "Finance", "Education", "Environment", "Security", "IT", "Other"].index(incident.get_category()),
            key=f"cat_{incident.get_id()}"
        )

        new_size = st.number_input(
            "Size (MB)",
            value=incident.calculate_size_mb(),
            key=f"size_{incident.get_id()}"
        )

        # Update button
        if st.button("Update", key=f"update_{incident.get_id()}"):
            db.update_dataset_incident(
                incident.get_id(),
                new_source,
                new_category,
                new_size
            )
            st.success("Incident updated.")
            st.rerun()

        # Delete button
        if st.button("🗑 Delete", key=f"delete_{incident.get_id()}"):
            db.delete_dataset_incident(incident.get_id())
            st.warning("Incident deleted.")
            st.rerun()


df = pd.DataFrame([{
    "id": ds.get_id(),
    "name": ds.get_name(),
    "source": ds.get_source(),
    "category": ds.get_category(),
    "size": ds.calculate_size_mb()
} for ds in incidents])


# Graphs
graph_type = st.selectbox(
    "Select Graph Type:",
    ["Bar Chart — Category Counts", "Pie Chart — Source Breakdown", "Line Chart — Size Trend"]
)


if graph_type == "Bar Chart — Category Counts":
    counts = df["category"].value_counts()
    fig, ax = plt.subplots()
    ax.bar(counts.index, counts.values, color="skyblue")
    ax.set_title("Datasets per Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Count")
    st.pyplot(fig)

elif graph_type == "Pie Chart — Source Breakdown":
    counts = df["source"].value_counts()
    fig, ax = plt.subplots()
    ax.pie(counts.values, labels=counts.index, autopct="%1.1f%%", startangle=90)
    ax.set_title("Datasets by Source")
    st.pyplot(fig)

elif graph_type == "Line Chart — Size Trend":
    #sort by size or id
    df_sorted = df.sort_values("id")
    chart = px.line(df_sorted, x="id", y="size", markers=True,
                    title="Dataset Size Trend (MB)", labels={"size":"Size (MB)", "id":"Dataset ID"})
    st.plotly_chart(chart)


#Streamlit UI


#	Initialize	OpenAI	client 
client = OpenAI(api_key	= st.secrets["OPENAI_API_KEY"] )

	 
#	Page	title 
st.title(" Data Science AI Assistant") 
	 
#	Initialize	session	state	for	messages 
if 'messages' not in st.session_state: 
    st.session_state.messages = [ 
        { 
		 "role": "system", 
		 "content": """You	are	a	data	science	expert	assistant.
            1. Provide	concise	and	accurate	information	related	to	data	science.
            2. Answer	questions	about	data	analysis,	visualization,	machine learning,	statistical	methods,	and	related	topics.
            3. Use	simple	language	and	examples	where	possible.
            4. If	you	don't	know	the	answer,	admit	it	instead	of	making	up	information.
            5. Stay	up-to-date	with	the	latest	trends	and	technologies	in	data	science."""
        }
    ]        
	             
	 
#	Display	all	previous	messages 
for	message	in	st.session_state.messages: 
	if	message["role"]	!=	"system":		#	Don't	display	system	prompt
		with	st.chat_message(message["role"]): 
			st.markdown(message["content"]) 
	 
#	Get	user	input 
prompt	= st.chat_input("Ask about Data Science...") 
	 
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
    
