# history_sales_routes.py
import streamlit as st
from db_connector import get_connection

def get_history_sales():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Select relevant columns from history_sales and drugs tables
            cursor.execute("""
                SELECT hs.*, d.name as drug_name
                FROM history_sales hs
                JOIN drugs d ON hs.drug_id = d.id;
            """)
            # Fetch column names from cursor.description
            column_names = [column[0] for column in cursor.description]
            # Fetch all rows including column names
            result = [dict(zip(column_names, row)) for row in cursor.fetchall()]
    finally:
        connection.close()
    return result

def edit_history_sale(history_sale_id, new_quantity):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Update the quantity for the specified history sale ID
            cursor.execute("UPDATE history_sales SET quantity_sold = %s WHERE id = %s;", (new_quantity, history_sale_id))
            
            # Recalculate the total_amount based on the new quantity
            cursor.execute("""
                UPDATE history_sales hs
                JOIN drugs d ON hs.drug_id = d.id
                SET hs.total_amount = hs.quantity_sold * d.unit_price
                WHERE hs.id = %s;
            """, (history_sale_id,))
            
        connection.commit()
    finally:
        connection.close()

def history_sales_page():
    st.title("History Sales")

    # Fetch history sales records
    history_sales = get_history_sales()

    # Display history sales records in a DataFrame
    st.dataframe(history_sales)

    # Add "Edit" and "Delete" options
    selected_sale_id = st.text_input("Enter the ID of the sale you want to edit or delete:")
    new_quantity = st.text_input("Enter the new quantity for editing:")

    if st.button("Edit"):
        if selected_sale_id and new_quantity:
            edit_history_sale(int(selected_sale_id), int(new_quantity))
            st.success("Sale edited successfully!")
        else:
            st.warning("Please enter both the sale ID and the new quantity.")
