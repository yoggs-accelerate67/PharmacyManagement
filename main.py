# main.py
import streamlit as st 
from admin_page import admin_page
from login_routes import login_page
from invoice_routes import invoice_page
from user_routes import users_page
from drug_routes import drugs_page
from sales_routes import sales_page
from history_sales_routes import history_sales_page
from company_routes import company_page  # Import the new company page
from db_connector import get_connection

# Initialize session state
def init_session_state():
    st.session_state.setdefault('authenticated', False)
    st.session_state.setdefault('user_id', None) 

# Function to run a database query
def run_database_query(query):
    # Replace these with your actual database connection details
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Notyou@1910',
        'database': 'DrugManagement',
    }

    # Connect to the database
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            # Execute the query
            cursor.execute(query)
            # Fetch the result
            result = cursor.fetchall()
    finally:
        # Close the database connection
        connection.close()

    return result

# Main function
def main():
    init_session_state()
    st.title("MedTrack Management")

    # Check if the user is authenticated
    authenticated = st.session_state.authenticated

    # If not authenticated, show the Admin page (authentication)
    if not authenticated:
        authenticated = admin_page()  # Update 'authenticated' based on login_page result

        if authenticated:
            st.session_state.authenticated = True  # Update session_state if login is successful

    # If authenticated, show the main content
    if authenticated:
        # Add a logout button to the left sidebar
        st.sidebar.button("Logout", on_click=logout)

        # Add navigation to different pages
        page = st.sidebar.selectbox("Select a page", ["Company", "Drugs", "Sales", "Invoice", "History Sales", "Users"])


        if page == "Company":
            company_page()  # Display the new company page
        elif page == "Drugs":
            drugs_page()
        elif page == "Sales":
            sales_page()
        elif page == "Invoice":
            invoice_page()
        elif page == "History Sales":
            history_sales_page()  # Display the history sales page
        elif page == "Users":
            users_page()


        # Add a text input and a "Run Query" button to the sidebar
        query = st.sidebar.text_input("Enter SQL Query")
        if st.sidebar.button("Run Query"):
            # Run the query using the function
            result = run_database_query(query)
            st.sidebar.write("Query Result:", result)

# Function to handle logout
def logout():
    st.session_state.authenticated = False
    st.success("Logout successful!")

if __name__ == "__main__":
    main()
