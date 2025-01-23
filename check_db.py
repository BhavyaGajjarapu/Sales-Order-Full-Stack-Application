import sqlite3

# Connect to the database file
conn = sqlite3.connect('sales.db')
cursor = conn.cursor()

# Check if the tables exist
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

if tables:
    print("Tables in the database:", tables)
else:
    print("No tables found. You may need to initialize the database.")

# Close the connection
conn.close()
