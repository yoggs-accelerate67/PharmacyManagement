# setup_database.py
import pymysql  # Adjust the import based on your database connector

def setup_database():
    # Connect to the database
    connection = pymysql.connect(host='localhost', user='root', password='moksh@99', database='drugsmanagement')

    # Execute the setup scripts
    # Example in setup_database.py
    with open(r"C:\Users\RMK KOUSHIK\Downloads\Pharmacy\create_tables.sql", 'r') as file:
     create_tables_sql = file.read()


    with open(r'C:\Users\RMK KOUSHIK\Downloads\Pharmacy\create_trigger.sql', 'r') as file:
        trigger_sql = file.read()
        with connection.cursor() as cursor:
            cursor.execute(trigger_sql)

    with open(r'C:\Users\RMK KOUSHIK\Downloads\Pharmacy\create_procedure.sql', 'r') as file:
        procedure_sql = file.read()
        with connection.cursor() as cursor:
            cursor.execute(procedure_sql)

    

    # Commit the changes and close the connection
    connection.commit()
    connection.close()
