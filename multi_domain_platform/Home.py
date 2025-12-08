import streamlit as st

st.set_page_config(
    page_title="Dashboard",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Welcome to the Platform Dashboard")

st.write("This is your main landing page before logging in.")

st.markdown("---")

# Dashboard content
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Users", "120")
    st.progress(80)

with col2:
    st.metric("Active Sessions", "14")
    st.progress(30)

with col3:
    st.metric("System Health", "Good")
    st.progress(100)

st.markdown("---")

# Go to login page
st.subheader("🔐 Please log in to continue")

if st.button("Go to Login Page"):
    st.switch_page("pages/1_Login.py")
