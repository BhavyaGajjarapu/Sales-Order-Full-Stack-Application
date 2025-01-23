import sqlite3

def initialize_database():
    conn = sqlite3.connect('sales.db')
    cursor = conn.cursor()

    # Drop existing tables if they exist
    cursor.execute('DROP TABLE IF EXISTS SalesOrderLine')
    cursor.execute('DROP TABLE IF EXISTS SalesOrder')

    # Create SalesOrder table
    cursor.execute('''
    CREATE TABLE SalesOrder (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        SalesOrderNumber INTEGER UNIQUE,
        CustomerName TEXT,
        OrderDate TEXT,
        TotalAmount REAL
    )
    ''')

    # Create SalesOrderLine table
    cursor.execute('''
    CREATE TABLE SalesOrderLine (
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

# Run this file once to initialize or reinitialize the database
initialize_database()
