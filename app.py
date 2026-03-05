from flask import Flask, request, jsonify, send_file
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("students.db")
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
    conn.close()

init_db()


@app.route("/")
def home():
    return send_file("app.html")


@app.route("/add_student", methods=["POST"])
def add_student():

    data = request.json

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR REPLACE INTO students VALUES (?,?,?,?)",
        (data["sap"], data["name"], data["age"], data["marks"])
    )

    conn.commit()
    conn.close()

    return jsonify({"message":"Student added"})


@app.route("/get_student/<sap>")
def get_student(sap):

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE sap=?", (sap,))
    student = cursor.fetchone()

    conn.close()

    if student:
        return jsonify({
            "sap":student[0],
            "name":student[1],
            "age":student[2],
            "marks":student[3]
        })

    return jsonify({"message":"Student not found"})


if __name__ == "__main__":
    app.run(debug=True)