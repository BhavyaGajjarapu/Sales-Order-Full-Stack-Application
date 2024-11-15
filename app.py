import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Utility function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('sales.db')
    conn.row_factory = sqlite3.Row  # to return dictionary-like rows
    return conn

# Route to display Sales Orders
@app.route('/')
def index():
    conn = get_db_connection()
    sales_orders = conn.execute('SELECT * FROM SalesOrder').fetchall()
    conn.close()
    return render_template('sales_order.html', sales_orders=sales_orders)

# Route to display items for a specific Sales Order
@app.route('/sales_order_line/<int:sales_order_id>', methods=['GET', 'POST'])
def sales_order_line(sales_order_id):
    conn = get_db_connection()

    # Get the search query from the form
    search_query = request.form.get('search_query', '')

    if search_query:
        # If there's a search query, filter by ItemCode or ItemName
        sales_order_lines = conn.execute(''' 
            SELECT * FROM SalesOrderLine 
            WHERE SalesOrderId = ? AND (ItemCode LIKE ? OR ItemName LIKE ?)
        ''', (sales_order_id, f'%{search_query}%', f'%{search_query}%')).fetchall()
    else:
        # If no search query, fetch all records for this SalesOrderId
        sales_order_lines = conn.execute('SELECT * FROM SalesOrderLine WHERE SalesOrderId = ?', (sales_order_id,)).fetchall()

    # Calculate total items, total quantity, and total price
    total_items = len(sales_order_lines)
    total_qty = sum(line['Qty'] for line in sales_order_lines)
    total_price = sum(line['TotalPrice'] for line in sales_order_lines)

    conn.close()

    return render_template('sales_order_line.html', 
                           sales_order_id=sales_order_id, 
                           sales_order_lines=sales_order_lines, 
                           total_items=total_items, 
                           total_qty=total_qty, 
                           total_price=total_price, 
                           search_query=search_query)

# Route to add a new Sales Order
@app.route('/add_sales_order', methods=['GET', 'POST'])
def add_sales_order():
    if request.method == 'POST':
        sales_order_number = request.form['SalesOrderNumber']
        customer_name = request.form['CustomerName']
        order_date = request.form['OrderDate']
        total_amount = request.form['TotalAmount']

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO SalesOrder (SalesOrderNumber, CustomerName, OrderDate, TotalAmount)
            VALUES (?, ?, ?, ?)
        ''', (sales_order_number, customer_name, order_date, total_amount))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('add_sales_order.html')

# Route to edit a Sales Order
@app.route('/edit_sales_order/<int:id>', methods=['GET', 'POST'])
def edit_sales_order(id):
    conn = get_db_connection()
    sales_order = conn.execute('SELECT * FROM SalesOrder WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        sales_order_number = request.form['SalesOrderNumber']
        customer_name = request.form['CustomerName']
        order_date = request.form['OrderDate']
        total_amount = request.form['TotalAmount']

        conn.execute('''
            UPDATE SalesOrder SET SalesOrderNumber = ?, CustomerName = ?, OrderDate = ?, TotalAmount = ?
            WHERE id = ?
        ''', (sales_order_number, customer_name, order_date, total_amount, id))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('edit_sales_order.html', sales_order=sales_order)

# Route to delete a Sales Order
@app.route('/delete_sales_order/<int:id>', methods=['GET'])
def delete_sales_order(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM SalesOrder WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Route to add a new Sales Order Line
@app.route('/add_sales_order_line/<int:sales_order_id>', methods=['GET', 'POST'])
def add_sales_order_line(sales_order_id):
    if request.method == 'POST':
        item_code = request.form['ItemCode']
        item_name = request.form['ItemName']
        unit_price = request.form['UnitPrice']
        qty = request.form['Qty']
        total_price = float(unit_price) * int(qty)

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO SalesOrderLine (SalesOrderId, ItemCode, ItemName, UnitPrice, Qty, TotalPrice)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (sales_order_id, item_code, item_name, unit_price, qty, total_price))
        conn.commit()
        conn.close()

        return redirect(url_for('sales_order_line', sales_order_id=sales_order_id))

    return render_template('add_sales_order_line.html', sales_order_id=sales_order_id)

# Route to edit a Sales Order Line
@app.route('/edit_sales_order_line/<int:id>', methods=['GET', 'POST'])
def edit_sales_order_line(id):
    conn = get_db_connection()
    sales_order_line = conn.execute('SELECT * FROM SalesOrderLine WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        item_code = request.form['ItemCode']
        item_name = request.form['ItemName']
        unit_price = request.form['UnitPrice']
        qty = request.form['Qty']
        total_price = float(unit_price) * int(qty)

        conn.execute('''
            UPDATE SalesOrderLine SET ItemCode = ?, ItemName = ?, UnitPrice = ?, Qty = ?, TotalPrice = ?
            WHERE id = ?
        ''', (item_code, item_name, unit_price, qty, total_price, id))
        conn.commit()
        conn.close()

        return redirect(url_for('sales_order_line', sales_order_id=sales_order_line['SalesOrderId']))

    return render_template('edit_sales_order_line.html', sales_order_line=sales_order_line)

# Route to delete a Sales Order Line
@app.route('/delete_sales_order_line/<int:id>', methods=['GET'])
def delete_sales_order_line(id):
    conn = get_db_connection()
    sales_order_line = conn.execute('SELECT * FROM SalesOrderLine WHERE id = ?', (id,)).fetchone()
    sales_order_id = sales_order_line['SalesOrderId']

    conn.execute('DELETE FROM SalesOrderLine WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('sales_order_line', sales_order_id=sales_order_id))

if __name__ == '__main__':
    app.run(debug=True)
