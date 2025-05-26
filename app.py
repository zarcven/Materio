from flask import Flask, send_from_directory, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__, static_folder="javascript-version/dist", static_url_path="")
CORS(app)

# Serve frontend
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

# Connect to DB helper
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="northwind"
    )

# Inventory Transactions
@app.route("/api/inventory-transactions")
def get_inventory_transactions():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT transaction_created_date, quantity FROM inventory_transactions")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(results)
    except Exception as e:
        print("❌ Error fetching inventory:", e)
        return jsonify({"error": str(e)}), 500

# Order Details
@app.route("/api/order-details")
def get_order_details():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT order_id FROM order_details")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(results)
    except Exception as e:
        print("❌ Error fetching orders:", e)
        return jsonify({"error": str(e)}), 500

# Customers
@app.route("/api/customers")
def get_customers():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT job_title FROM customers")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(results)
    except Exception as e:
        print("❌ Error fetching customers:", e)
        return jsonify({"error": str(e)}), 500

# Employees
@app.route("/api/employees")
def get_employees():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT job_title FROM employees")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(results)
    except Exception as e:
        print("❌ Error fetching employees:", e)
        return jsonify({"error": str(e)}), 500

# Products
@app.route("/api/products")
def get_products():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT category FROM products")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(results)
    except Exception as e:
        print("❌ Error fetching products:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
