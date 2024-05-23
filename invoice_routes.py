# invoice_routes.py
import streamlit as st
from db_connector import get_connection
from fpdf import FPDF

class InvoicePDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, 'MedTrack Pharmaceuticals', 0, 1, 'C', 1)
        self.ln(10)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 16)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body, 1)
        self.ln(4)

def view_last_transaction():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Fetch the details of the last transaction from the sales table
        cursor.execute("SELECT s.*, c.id as manufacturer_id, c.phone_number FROM sales s JOIN company c ON s.manufacturer_id = c.id ORDER BY s.sale_date DESC LIMIT 1")
        last_transaction = cursor.fetchone()
    finally:
        connection.close()

    return last_transaction

def generate_invoice_pdf(last_transaction):
    pdf = InvoicePDF()
    pdf.add_page()

    # Style the header and title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'MedTrack Pharmaceuticals', 0, 1, 'C')  # Center align
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Invoice', 0, 1, 'L')  # Left align
    pdf.ln(10)

    # Style the body content
    pdf.set_font('Arial', '', 12)
    pdf.cell(40, 5, 'Transaction ID:', 0, 0)
    pdf.cell(50, 5, str(last_transaction[0]), 0, 1)
    pdf.cell(40, 5, 'Drug ID:', 0, 0)
    pdf.cell(50, 5, str(last_transaction[1]), 0, 1)
    pdf.cell(40, 5, 'Quantity Sold:', 0, 0)
    pdf.cell(50, 5, str(last_transaction[3]), 0, 1)
    pdf.cell(40, 5, 'Total Amount:', 0, 0)
    pdf.cell(50, 5, str(last_transaction[4]), 0, 1)
    pdf.cell(40, 5, 'Sale Date:', 0, 0)
    pdf.cell(50, 5, str(last_transaction[5].strftime('%Y-%m-%d')), 0, 1)  # Format the date
    pdf.cell(40, 5, 'Manufacturer ID:', 0, 0)
    pdf.cell(50, 5, str(last_transaction[6]), 0, 1)
    pdf.cell(40, 5, 'Manufacturer Phone:', 0, 0)
    pdf.cell(50, 5, str(last_transaction[7]), 0, 1)
    pdf.ln(10)

    # Create a visual separator
    pdf.line(10, 180, 200, 180)

    # Save the PDF to a file
    pdf_output_path = "invoice.pdf"
    pdf.output(pdf_output_path)

    return pdf_output_path

def invoice_page():
    st.subheader("Invoice Management")

    # View the details of the last transaction
    last_transaction = view_last_transaction()

    if last_transaction:
        st.write("Last Transaction Details:")
        st.write(f"Transaction ID: {last_transaction[0]}")
        st.write(f"Drug ID: {last_transaction[1]}")
        st.write(f"Quantity Sold: {last_transaction[3]}")
        st.write(f"Total Amount: {last_transaction[4]}")
        st.write(f"Sale Date: {last_transaction[5].strftime('%Y-%m-%d')}")
        st.write(f"Manufacturer ID: {last_transaction[6]}")
        st.write(f"Manufacturer Phone: {last_transaction[7]}")

        # Use a separate variable to control the download action
        download_invoice = st.button("Generate Invoice")

        # Add a button to download the invoice as PDF
        if download_invoice:
            # Generate and download the PDF
            pdf_path = generate_invoice_pdf(last_transaction)
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="CLICK TO DOWNLOAD AS PDF",
                    data=f.read(),
                    file_name="invoice.pdf",
                    key="download_button"
                )

    else:
        st.warning("No transactions available.")
