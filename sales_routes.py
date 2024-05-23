# sales_routes.py
import streamlit as st
from db_connector import get_connection
from login_routes import get_current_user_id

def sales_page():
    st.subheader("Sales Page")

    # Fetch drugs and manufacturers for dropdowns
    drugs = fetch_drugs()
    manufacturers = fetch_manufacturers()

    # Fetch usernames for dropdown
    usernames = fetch_usernames()

    # Collect sales details
    drug_name = st.selectbox("Select Drug", drugs)
    quantity = st.number_input("Quantity Sold", min_value=1, value=1)
    manufacturer_name = st.selectbox("Select Manufacturer", manufacturers)

    # Fetch unit price and manufacturer_id for the selected drug and manufacturer
    unit_price, manufacturer_id = fetch_unit_price_and_manufacturer_id(drug_name, manufacturer_name)

    # Check if unit_price is None
    if unit_price is None:
        st.warning("Please select a manufacturer to calculate the total amount.")
        return

    # Get the current user's ID from the dropdown menu
    selected_username = st.selectbox("Select Username", usernames)
    pharmacist_id = get_current_user_id(selected_username)

    if pharmacist_id is None:
        return

    # Calculate total amount
    total_amount = quantity * unit_price

    # Display the dynamically updating total amount
    total_amount_display = st.empty()
    total_amount_display.text(f"Total Amount: {total_amount}")

    if st.button("Record Sale"):
        # Save the sales details to the database
        save_sale(drug_name, quantity, total_amount, manufacturer_id, pharmacist_id)

        st.success("Sale recorded successfully!")

    # Update the total amount display dynamically as quantity changes
    total_amount_display.text(f"Total Amount: {quantity * unit_price}")

# ... (rest of the code remains unchanged)

def fetch_usernames():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Fetch usernames from the login table
        cursor.execute("SELECT username FROM login")
        usernames = [row[0] for row in cursor.fetchall()]
        return usernames

    finally:
        connection.close()
def save_sale(drug_name, quantity, total_amount, manufacturer_id, pharmacist_id):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        drug_id = get_drug_id(drug_name)

        # Save the sale details to the sales table
        cursor.execute("INSERT INTO sales (drug_id, manufacturer_id, quantity, total_amount, sale_date, pharmacist_id) VALUES (%s, %s, %s, %s, CURDATE(), %s)", (drug_id, manufacturer_id, quantity, total_amount, pharmacist_id))
        connection.commit()

        # Save the sale details to the history_sales table
        cursor.execute("INSERT INTO history_sales (drug_id, manufacturer_id, quantity_sold, total_amount, sale_date, pharmacist_id) VALUES (%s, %s, %s, %s, CURDATE(), %s)", (drug_id, manufacturer_id, quantity, total_amount, pharmacist_id))
        connection.commit()

        st.success("Sale recorded successfully!")

    except Exception as e:
        st.error(f"Error recording sale: {str(e)}")

    finally:
        connection.close()

def fetch_drugs():
    connection = get_connection()
    cursor = connection.cursor()

    # Fetch drug names from the drugs table
    cursor.execute("SELECT name FROM drugs")
    drugs = [row[0] for row in cursor.fetchall()]

    connection.close()
    return drugs

def fetch_manufacturers():
    connection = get_connection()
    cursor = connection.cursor()

    # Fetch manufacturer names from the company table
    cursor.execute("SELECT name FROM company")
    manufacturers = [row[0] for row in cursor.fetchall()]

    connection.close()
    return manufacturers

def fetch_unit_price_and_manufacturer_id(drug_name, manufacturer_name):
    connection = get_connection()
    cursor = connection.cursor()

    # Fetch unit price and manufacturer_id for the selected drug and manufacturer
    cursor.execute("SELECT d.unit_price, c.id FROM drugs d INNER JOIN company c ON d.manufacturer_id = c.id WHERE d.name=%s AND c.name=%s", (drug_name, manufacturer_name))
    result = cursor.fetchone()

    connection.close()

    return result if result else (None, None)

def get_drug_id(drug_name):
    connection = get_connection()
    cursor = connection.cursor()

    # Retrieve the drug_id for the selected drug name
    cursor.execute("SELECT id FROM drugs WHERE name=%s", (drug_name,))
    drug_id = cursor.fetchone()[0]

    connection.close()
    return drug_id

