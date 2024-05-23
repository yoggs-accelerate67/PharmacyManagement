# company_routes.py
import streamlit as st
from db_connector import get_connection

def get_companies():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name, location, industry, phone_number FROM company;")
            result = cursor.fetchall()
    finally:
        connection.close()
    return result

def company_page():
    st.title("Company Page")

    # Add company-related functionality here using st components
    name = st.text_input("Company Name:")
    location = st.text_input("Location:")
    industry = st.text_input("Industry:")
    phone_number = st.text_input("Phone Number (10 digits):")

    if st.button("Add Company"):
        # You can use the database connection from db_connector.py
        connection = get_connection()

        # Perform database operations here (sample code)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO company (name, location, industry, phone_number) VALUES (%s, %s, %s, %s)",
                       (name, location, industry, phone_number))
        connection.commit()

        st.success("Company added successfully!")

        # Close the connection when done
        connection.close()

    # Display the list of companies
    companies = get_companies()
    st.subheader("List of Companies")
    if companies:
        for company in companies:
            st.write(f"ID: {company[0]}, Name: {company[1]}, Location: {company[2]}, Industry: {company[3]}, Phone Number: {company[4]}")
    else:
        st.write("No companies found.")
