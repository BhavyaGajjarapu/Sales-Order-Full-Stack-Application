# Sales Order Management System
A simple, full-stack web application built with Flask and SQLite3 to manage sales orders and their associated items.
The system allows users to:
* Create, view, edit, and delete sales orders.
* Manage items (sales order lines) within a sales order.
* Search items by ItemCode or ItemName.
* View totals, including the number of items, total quantity, and total price for each sales order.
# Project Structure

sales-order-management/
* app.py                 ----> Flask application
* sales.db               ----> SQLite database file (auto-created after setup)
* templates/             ----> HTML templates for rendering pages
  * sales_order.html     ----> Main page for Sales Orders
  * add_sales_order.html   ----> Form to add a new Sales Order
  * edit_sales_order.html  ----> Form to edit an existing Sales Order
  * sales_order_line.html  ----> Page for viewing and managing Sales Order Lines
  * add_sales_order_line.html ----> Form to add a new Sales Order Line
  * edit_sales_order_line.html ----> Form to edit an existing Sales Order Line
* static/                ----> Static files (CSS, JS, images)(optional)
  * styles.css         ----> Custom styling(optional)
# Features
# Sales Orders
* View all sales orders with key details.
* Add new sales orders.
* Edit existing sales orders.
* Delete sales orders.
# Sales Order Lines
* View all items for a specific sales order.
* Add new items to a sales order.
* Edit or delete existing items.
* Search items by ItemCode or ItemName.
# Display totals:
* Total number of items.
* Total quantity of items.
* Total price.
# Technologies Used
* Backend Framework: Flask
* Database: SQLite3
* Frontend: HTML, CSS (Bootstrap for styling)
