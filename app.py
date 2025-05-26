from flask import Flask, send_from_directory
import mysql.connector

app = Flask(__name__, static_folder="javascript-version/dist", static_url_path="")

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/api/customers")
def get_customers():
    conn = mysql.connector.connect(
        host="your-db-host",           # UPDATE this
        user="your-db-username",       # UPDATE this
        password="your-db-password",   # UPDATE this
        database="your-db-name"        # UPDATE this
    )
    cursor = conn.cursor()
    cursor.execute("SELECT CustomerID, CompanyName FROM Customers")
    results = cursor.fetchall()
    conn.close()
    return {"customers": results}

if __name__ == "__main__":
    app.run(debug=True)
