# register.py
import streamlit as st
from db_connector import get_connection

def registration_page():
    st.subheader("Register")

    # Add registration-related functionality here using st components
    new_username = st.text_input("New Username:")
    new_password = st.text_input("New Password:", type="password")

    if st.button("Register"):
        # You can use the database connection from db_connector.py
        connection = get_connection()

        # Perform user registration here (sample code)
        cursor = connection.cursor()

        try:
            # Check if the username already exists
            cursor.execute("SELECT * FROM login WHERE username=%s", (new_username,))
            result = cursor.fetchone()

            if result:
                st.error("Username already exists. Choose a different username.")
            else:
                # Fetch the maximum 'id' from the 'users' table
                cursor.execute("SELECT MAX(id) FROM users")
                last_user_id = cursor.fetchone()[0]

                # If there are no users yet, set last_user_id to 1
                last_user_id = last_user_id  if last_user_id is not None else 1

                # Insert the new user into the 'login' table
                cursor.execute("INSERT INTO login (id, username, password) VALUES (%s, %s, %s)",
                               (last_user_id, new_username, new_password))
                connection.commit()

                st.success("Registration successful! You can now login.")

        except Exception as e:
            st.error(f"Error during registration: {str(e)}")

        finally:
            # Close the connection when done
            connection.close()

    return False
