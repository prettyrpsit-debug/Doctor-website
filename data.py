from flask import Flask, render_template_string
from db import get_db_connection

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Database Dashboard</title>

    <style>
        body{
            font-family:Arial;
            background:#f4f4f4;
            padding:20px;
        }

        h1{
            text-align:center;
            color:purple;
        }

        table{
            width:100%;
            border-collapse:collapse;
            background:white;
        }

        th{
            background:purple;
            color:white;
            padding:12px;
        }

        td{
            padding:10px;
            border:1px solid #ddd;
            text-align:center;
        }

        tr:nth-child(even){
            background:#f9f9f9;
        }

        tr:hover{
            background:#eeeeee;
        }
    </style>
</head>

<body>

<h1>Hospital Appointment Database</h1>

<table>

<tr>
    <th>ID</th>
    <th>Patient Name</th>
    <th>Phone</th>
    <th>Appointment Date</th>
    <th>Doctor</th>
    <th>Symptoms</th>
</tr>

{% for row in data %}
<tr>
    <td>{{ row[0] }}</td>
    <td>{{ row[1] }}</td>
    <td>{{ row[2] }}</td>
    <td>{{ row[3] }}</td>
    <td>{{ row[4] }}</td>
    <td>{{ row[5] }}</td>
</tr>
{% endfor %}

</table>

</body>
</html>
"""

@app.route("/")
def dashboard():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM appointments ORDER BY id ASC")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template_string(HTML, data=data)

if __name__ == "__main__":
    app.run(debug=True, port=5001)