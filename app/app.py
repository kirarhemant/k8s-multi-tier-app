from flask import Flask, jsonify
import mysql.connector
from mysql.connector import pooling
import os
import time

app = Flask(__name__)

# Database configuration from environment variables
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "pool_name": "api_pool",
    "pool_size": 5,  # Number of connections in pool
    "pool_reset_session": True
}

# Create connection pool
db_pool = pooling.MySQLConnectionPool(**DB_CONFIG)

def get_db_connection():
    """Get a connection from the pool with retry logic"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return db_pool.get_connection()
        except mysql.connector.Error as err:
            print(f"Connection failed (attempt {attempt + 1}): {err}")
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait before retrying
            continue
    raise Exception("Failed to get DB connection after retries")

@app.route('/products')
def get_products():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        return jsonify(products)
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": "Database operation failed"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()  # Returns connection to pool

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)