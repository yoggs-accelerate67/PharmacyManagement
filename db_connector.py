# db_connector.py
import mysql.connector

# Replace with your database credentials
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Notyou@1910",
    "database": "DrugManagement",
}

def get_connection():
    return mysql.connector.connect(**db_config)
