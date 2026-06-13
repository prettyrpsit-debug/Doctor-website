from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Create Database Table
def init_db():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT NOT NULL,
        phone TEXT NOT NULL,
        appointment_date TEXT NOT NULL,
        doctor TEXT NOT NULL,
        symptoms TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/appointment", methods=["POST"])
def appointment():

    patient_name = request.form["patient_name"]
    phone = request.form["phone"]
    appointment_date = request.form["appointment_date"]
    doctor = request.form["doctor"]
    symptoms = request.form["symptoms"]

    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO appointments
    (patient_name, phone, appointment_date, doctor, symptoms)
    VALUES (?, ?, ?, ?, ?)
    """,
    (patient_name, phone, appointment_date, doctor, symptoms))

    conn.commit()
    conn.close()

    return """
    <script>
    alert('Appointment Booked Successfully!');
    window.location.href='/';
    </script>
    """


@app.route("/appointments")
def appointments():

    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM appointments")
    data = cursor.fetchall()

    conn.close()

    return str(data)


if __name__ == "__main__":
    app.run(debug=True)