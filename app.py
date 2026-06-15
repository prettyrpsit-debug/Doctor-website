from flask import Flask, render_template, request, redirect, url_for
from db import get_db_connection, init_db, fetch_all_as_dict

app = Flask(__name__)

# Initialize PostgreSQL Database Table
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

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO appointments
    (patient_name, phone, appointment_date, doctor, symptoms)
    VALUES (%s, %s, %s, %s, %s)
    """,
    (patient_name, phone, appointment_date, doctor, symptoms))

    conn.commit()
    cursor.close()
    conn.close()

    return """
    <script>
    alert('Appointment Booked Successfully!');
    window.location.href='/';
    </script>
    """


@app.route("/appointments")
def appointments():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM appointments ORDER BY id ASC")
    data = fetch_all_as_dict(cursor)

    cursor.close()
    conn.close()

    return render_template("dashboard.html", appointments=data)


if __name__ == "__main__":
    app.run(debug=True)