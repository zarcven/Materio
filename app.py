from flask import Flask, send_from_directory, jsonify
import mysql.connector

app = Flask(__name__, static_folder="javascript-version/dist", static_url_path="")

# Serve frontend
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

# Sample API to get customers
@app.route("/api/customers")
def get_customers():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # since you have no password
            database="northwind"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT id, company FROM customers LIMIT 10")
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        customers = [{"id": row[0], "company": row[1]} for row in results]
        return jsonify(customers)

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True)
