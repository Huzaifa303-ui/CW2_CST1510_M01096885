import streamlit as st
import bcrypt

st.set_page_config(
    page_title="Login / Register",
    page_icon="🔑",
    layout="centered"
)

#Session State Setup
if "users" not in st.session_state:
    st.session_state.users = {}  # {username: bcrypt_hash}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""


# DASHBOARD (shown only after login)
if st.session_state.logged_in:

    st.title(f"👋 Welcome, {st.session_state.username}!")
    st.subheader("Choose a section")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🛡 Cybersecurity"):
            st.switch_page("pages/2_Cybersecurity.py")

        if st.button("🤖 AI Assistant"):
            st.switch_page("pages/4_AI_Assistant.py")

    with col2:
        if st.button("💻 IT Operations"):
            st.switch_page("pages/5_IT_Operations.py")

        if st.button("📊 Data Science"):
            st.switch_page("pages/3_Data_Science.py")

    st.markdown("---")

    if st.button("Log out"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    st.stop()


#  LOGIN + REGISTER PAGE 
st.title("🔐 Welcome")

tab_login, tab_register = st.tabs(["Login", "Register"])


# LOGIN TAB 
with tab_login:
    st.subheader("Login")

    login_username = st.text_input("Username")
    login_password = st.text_input("Password", type="password")

    if st.button("Log in", type="primary"):
        users = st.session_state.users

        if login_username not in users:
            st.error("Invalid username or password.")
        else:
            stored_hash = users[login_username]

            if bcrypt.checkpw(login_password.encode(), stored_hash.encode()):
                st.session_state.logged_in = True
                st.session_state.username = login_username
                st.rerun()   # Reload to show dashboard
            else:
                st.error("Invalid username or password.")


#  REGISTER TAB
with tab_register:
    st.subheader("Register")

    new_username = st.text_input("Choose a username")
    new_password = st.text_input("Choose a password", type="password")
    confirm_password = st.text_input("Confirm password", type="password")

    if st.button("Create account"):
        # Empty fields
        if not new_username or not new_password or not confirm_password:
            st.warning("Please fill in all fields.")

        # Username checks
        elif len(new_username) < 3:
            st.error("Username must be at least 3 characters.")

        elif len(new_username) > 20:
            st.error("Username cannot exceed 20 characters.")

        elif " " in new_username:
            st.error("Username cannot contain spaces.")

        elif not new_username[0].isalpha():
            st.error("Username must start with a letter.")

        elif not all(char.isalnum() or char == "_" for char in new_username):
            st.error("Username can only contain letters, numbers, and underscores.")

        elif new_username in st.session_state.users:
            st.error("Username already exists.")

        # Password checks
        elif len(new_password) < 6:
            st.error("Password must be at least 6 characters.")

        elif not any(char.isdigit() for char in new_password):
            st.error("Password must contain at least one number.")

        elif not any(char.isupper() for char in new_password):
            st.error("Password must contain at least one uppercase letter.")

        elif not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for char in new_password):
            st.error("Password must contain at least one special character.")

        elif new_password != confirm_password:
            st.error("Passwords do not match.")

        else:
            # Hash & save user
            hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            st.session_state.users[new_username] = hashed_pw

            st.success("Account created successfully! 🎉")
            st.info("Go to the Login tab to sign in.")
