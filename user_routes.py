import streamlit as st
from db_connector import get_connection

def users_page():
    st.title("Users Page")

    # Add users-related functionality here using st components
    first_name = st.text_input("First Name:")
    last_name = st.text_input("Last Name:")
    email = st.text_input("Email:")
    phone_number = st.text_input("Phone Number:")
    address = st.text_input("Address:")

    if st.button("Add User"):
        # You can use the database connection from db_connector.py
        connection = get_connection()

        try:
            # Perform database operations here (sample code)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (first_name, last_name, email, phone_number, address) VALUES (%s, %s, %s, %s, %s)",
                           (first_name, last_name, email, phone_number, address))
            connection.commit()

            st.success("User added successfully!")

        except Exception as e:
            st.error(f"Error adding user: {str(e)}")

        finally:
            # Close the connection when done
            connection.close()
