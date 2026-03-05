from flask import Flask, request, jsonify, send_file
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get("postgresql://students_user:MqxyJlO6ClCLAbuHvAm8gU9KARIOm4wf@dpg-d6kju356ubrc73ehsl9g-a/students_3e00")

def get_connection():
    return psycopg2.connect(DATABASE_URL)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        sap TEXT PRIMARY KEY,
        name TEXT,
        age INTEGER,
        marks INTEGER
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()

init_db()


@app.route("/")
def home():
    return send_file("app.html")


@app.route("/add_student", methods=["POST"])
def add_student():

    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO students (sap, name, age, marks)
        VALUES (%s,%s,%s,%s)
        ON CONFLICT (sap)
        DO UPDATE SET
        name = EXCLUDED.name,
        age = EXCLUDED.age,
        marks = EXCLUDED.marks
        """,
        (data["sap"], data["name"], data["age"], data["marks"])
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message":"Student added"})


@app.route("/get_student/<sap>")
def get_student(sap):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE sap=%s", (sap,))
    student = cursor.fetchone()

    cursor.close()
    conn.close()

    if student:
        return jsonify({
            "sap": student[0],
            "name": student[1],
            "age": student[2],
            "marks": student[3]
        })

    return jsonify({"message":"Student not found"})


if __name__ == "__main__":
    app.run(debug=True)