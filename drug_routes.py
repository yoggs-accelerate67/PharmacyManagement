# drugs_routes.py
import streamlit as st
from db_connector import get_connection

def get_drugs():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name, unit_price FROM drugs;")
            result = cursor.fetchall()
    finally:
        connection.close()
    return result

def get_manufacturers():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name FROM company;")
            result = cursor.fetchall()
    finally:
        connection.close()
    return result

def drugs_page():
    st.title("Drugs Page")

    # Add drugs-related functionality here using st components
    name = st.text_input("Drug Name:")
    
    # Get the list of manufacturers for dropdown
    manufacturers = get_manufacturers()
    manufacturer_options = [manufacturer[1] for manufacturer in manufacturers]
    selected_manufacturer_name = st.selectbox("Manufacturer:", manufacturer_options)

    expiration_date = st.date_input("Expiration Date:")
    unit_price = st.number_input("Unit Price:")

    if st.button("Add Drug"):
        # Find the selected manufacturer id
        selected_manufacturer = next((manufacturer for manufacturer in manufacturers if manufacturer[1] == selected_manufacturer_name), None)

        if selected_manufacturer:
            selected_manufacturer_id = selected_manufacturer[0]

            # You can use the database connection from db_connector.py
            connection = get_connection()

            # Perform database operations here (sample code)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO drugs (name, manufacturer_id, expiration_date, unit_price) VALUES (%s, %s, %s, %s)",
                           (name, selected_manufacturer_id, expiration_date, unit_price))
            connection.commit()

            st.success("Drug added successfully!")

            # Close the connection when done
            connection.close()
        else:
            st.error("Selected manufacturer not found in the database.")
