# login_routes.py
import streamlit as st
from db_connector import get_connection

def login_page():
    page_name = "login_page"  # Customize this based on your page structure

    st.subheader("Login")

    # Add login-related functionality here using st components
    username = st.text_input("Username", key=f"{page_name}_username_input")
    password = st.text_input("Password", type="password", key=f"{page_name}_password_input")

    button_clicked = st.button("Login", key=f"{page_name}_login_button")

    if button_clicked:
        # You can use the database connection from db_connector.py
        connection = get_connection()

        # Perform login authentication here (sample code)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM login WHERE username=%s AND password=%s", (username, password))
        result = cursor.fetchone()

        if result:
            st.success("Login successful!")

            # Store the user information in the session (you may need to implement this based on your session management)
            # Example: st.session_state.user_id = result["id"]

        else:
            st.error("Login failed. Invalid credentials.")

        # Close the connection when done
        connection.close()

        return result is not None  # True if login successful, False otherwise

    return False

def get_current_user_id():
    return st.session_state.user_id

def get_current_user_id(username):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Fetch the user_id from the login table based on the username
        cursor.execute("SELECT id FROM login WHERE username=%s", (username,))
        user_id = cursor.fetchone()

        if user_id:
            return user_id[0]
        else:
            st.warning("User not found.")
            return None

    finally:
        connection.close()
