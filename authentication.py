# authentication.py
import streamlit as st
from login_routes import login_page
from register import registration_page

def authentication_page():
    st.title("Authentication Page")

    # Check if the user has been authenticated
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    # If already authenticated, return True
    if st.session_state.authenticated:
        return True

    # Add authentication-related functionality here using st components
    action = st.radio("Choose an action", ["Login", "Register"])

    if action == "Login":
        authenticated = login_page()
    elif action == "Register":
        authenticated = registration_page()
    
    # Update the authenticated flag
    st.session_state.authenticated = authenticated

    return authenticated
