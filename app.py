from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
 
app = Flask(__name__)
 
DATABASE = "students.db"
 
# Create DB if not exists
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            studentname TEXT NOT NULL,
            sapid TEXT NOT NULL,
            gender TEXT NOT NULL,
            marks REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()
 
init_db()
 
 
@app.route("/")
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, studentname FROM students")
    students = cursor.fetchall()
    conn.close()
    return render_template("index.html", students=students)
 
 
@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        studentname = request.form["studentname"]
        sapid = request.form["sapid"]
        gender = request.form["gender"]
        marks = request.form["marks"]
 
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO students (studentname, sapid, gender, marks)
            VALUES (?, ?, ?, ?)
        """, (studentname, sapid, gender, marks))
        conn.commit()
        conn.close()
 
        return redirect(url_for("index"))
 
    return render_template("add_student.html")
 
 
@app.route("/student/<int:student_id>")
def student_detail(student_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
    student = cursor.fetchone()
    conn.close()
    return render_template("student_detail.html", student=student)
 
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)