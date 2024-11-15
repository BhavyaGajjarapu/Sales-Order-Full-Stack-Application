# database_setup.py
import sqlite3

def initialize_database():
    conn = sqlite3.connect('sales.db')
    cursor = conn.cursor()

    # Create SalesOrder table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS SalesOrder (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        SalesOrderNumber TEXT,
        CustomerName TEXT,
        OrderDate TEXT,
        TotalAmount REAL
    )
    ''')

    # Create SalesOrderLine table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS SalesOrderLine (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        SalesOrderId INTEGER,
        itemCode TEXT,
        itemName TEXT,
        UnitPrice REAL,
        Qty INTEGER,
        TotalPrice REAL,
        FOREIGN KEY(SalesOrderId) REFERENCES SalesOrder(id)
    )
    ''')

    conn.commit()
    conn.close()

# Run this file once to initialize the database
initialize_database()
