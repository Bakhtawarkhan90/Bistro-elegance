from flask import Flask, request, redirect, url_for, send_from_directory
import mysql.connector
import os
import time

app = Flask(__name__, static_url_path='/static', static_folder='.')

# 🔁 Connect to MySQL with retry
while True:
    try:
        db = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "database"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", "kali"),
            database=os.getenv("MYSQL_DATABASE", "table")   
        )
        print("✅ Database connected")
        break
    except mysql.connector.Error as err:
        print(f"❌ Database connection failed: {err}")
        time.sleep(5)

# 🧱 Create reserve table inside DB `table`
cursor = db.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS reserve (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    reservation_date DATE,
    reservation_time VARCHAR(20),
    guests INT,
    special_requests TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
cursor.close()

# 🏠 Serve main page
@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')

# 📥 Handle reservation form
@app.route('/reserve', methods=['POST'])
def reserve():
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    reservation_date = request.form.get('date')
    reservation_time = request.form.get('time')
    guests = request.form.get('guests')
    special_requests = request.form.get('special_requests')

    try:
        cursor = db.cursor()
        query = """
        INSERT INTO reserve
        (full_name, email, phone, reservation_date, reservation_time, guests, special_requests)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            full_name, email, phone,
            reservation_date, reservation_time,
            guests, special_requests
        )
        cursor.execute(query, values)
        db.commit()
        cursor.close()
        print("✅ Reservation saved:", values)
    except mysql.connector.Error as err:
        print(f"❌ Insert error: {err}")

    return redirect(url_for('thank_you'))

# ✅ Thank you page
@app.route('/thank_you')
def thank_you():
    return send_from_directory(os.getcwd(), 'thankyou.html')

# 📂 Serve static files
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.getcwd(), filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
