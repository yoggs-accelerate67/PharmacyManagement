# stock_routes.py
import streamlit as st
from db_connector import get_connection

def get_stock():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name, stock FROM drugs;")
            result = cursor.fetchall()
    finally:
        connection.close()
    return result

def reduce_stock(drug_id, quantity):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Get current stock
            cursor.execute("SELECT stock FROM drugs WHERE id = %s;", (drug_id,))
            current_stock = cursor.fetchone()['stock']

            # Reduce the stock by the sold quantity
            new_stock = max(0, current_stock - quantity)

            # Update the stock in the database
            cursor.execute("UPDATE drugs SET stock = %s WHERE id = %s;", (new_stock, drug_id))
        
        # Commit the transaction
        connection.commit()
    finally:
        connection.close()
def update_stock(drug_id, quantity):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE drugs
                SET stock = stock + %s
                WHERE id = %s;
            """, (quantity, drug_id))
        connection.commit()
        st.success("Stock updated successfully!")
    except Exception as e:
        st.error(f"Error updating stock: {e}")
    finally:
        connection.close()

def stock_page():
    st.title("Stock Page")

    # Fetch stock information
    stock_data = get_stock()

    # Display stock information
    st.write("Current Stock:")
    for drug in stock_data:
        st.write(f"{drug['name']}: {drug['stock']}")

    # Reduce stock based on sales (you may need to adapt this based on your sales logic)
    if st.button("Reduce Stock"):
        # Assuming you have a sales record, update this part based on your logic
        drug_id = st.number_input("Enter Drug ID:", min_value=1)
        quantity_sold = st.number_input("Enter Quantity Sold:", min_value=1)

        # Reduce the stock
        reduce_stock(drug_id, quantity_sold)
        st.success(f"Stock reduced for Drug ID {drug_id} by {quantity_sold} units.")

    # Check for low stock and display a reminder
    low_stock_threshold = 10  # Adjust this threshold as needed
    low_stock_drugs = [drug for drug in stock_data if drug['stock'] <= low_stock_threshold]

    if low_stock_drugs:
        st.warning("Low Stock Reminder:")
        for drug in low_stock_drugs:
            st.write(f"{drug['name']} has low stock: {drug['stock']} units remaining.")
