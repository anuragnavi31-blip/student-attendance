from flask import Flask, request, redirect
import sqlite3
from datetime import date

app = Flask(__name__)
DB = "attendance.db"

def db():
    return sqlite3.connect(DB)

def setup():
    con = db()
    con.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, roll TEXT, name TEXT, course TEXT)")
    con.execute("CREATE TABLE IF NOT EXISTS attendance (id INTEGER PRIMARY KEY, student_id INTEGER, day TEXT, status TEXT)")
    con.commit()
    con.close()

@app.route("/")
def home():
    setup()
    con = db()
    students = con.execute("SELECT * FROM students ORDER BY roll").fetchall()
    con.close()
    page = """<html><body style="font-family:Arial;margin:35px">
    <h1>Student Attendance Management System</h1>
    <h2>Add Student</h2>
    <form action="/add" method="post">
    Roll: <input name="roll" required> Name: <input name="name" required>
    Course: <input name="course" required> <button>Add Student</button></form>
    <h2>Students</h2><table border="1" cellpadding="8">
    <tr><th>Roll</th><th>Name</th><th>Course</th><th>Action</th></tr>"""
    for s in students:
        page += f"<tr><td>{s[1]}</td><td>{s[2]}</td><td>{s[3]}</td><td><a href='/mark/{s[0]}'>Mark attendance</a></td></tr>"
    page += "</table><p><a href='/report'>Attendance report</a></p></body></html>"
    return page

@app.route("/add", methods=["POST"])
def add():
    setup()
    con = db()
    con.execute("INSERT INTO students (roll,name,course) VALUES (?,?,?)",
                (request.form["roll"], request.form["name"], request.form["course"]))
    con.commit()
    con.close()
    return redirect("/")

@app.route("/mark/<int:sid>", methods=["GET", "POST"])
def mark(sid):
    setup()
    con = db()
    student = con.execute("SELECT * FROM students WHERE id=?", (sid,)).fetchone()
    if not student:
        con.close()
        return "Student not found", 404
    if request.method == "POST":
        con.execute("INSERT INTO attendance (student_id,day,status) VALUES (?,?,?)",
                    (sid, date.today().isoformat(), request.form["status"]))
        con.commit()
        con.close()
        return redirect("/")
    con.close()
    return f"""<html><body style="font-family:Arial;margin:35px"><h2>Attendance for {student[2]}</h2>
    <form method="post"><label><input type="radio" name="status" value="Present" required>Present</label>
    <label><input type="radio" name="status" value="Absent" required>Absent</label>
    <button>Save</button></form><p><a href="/">Back</a></p></body></html>"""

@app.route("/report")
def report():
    setup()
    con = db()
    rows = con.execute("""SELECT students.roll, students.name, attendance.day, attendance.status
    FROM attendance JOIN students ON students.id=attendance.student_id ORDER BY attendance.day DESC""").fetchall()
    con.close()
    page = "<html><body style='font-family:Arial;margin:35px'><h1>Attendance Report</h1><table border='1' cellpadding='8'><tr><th>Roll</th><th>Name</th><th>Date</th><th>Status</th></tr>"
    for r in rows:
        page += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
    return page + "</table><p><a href='/'>Back</a></p></body></html>"

@app.route("/health")
def health():
    return "Application is running", 200

if __name__ == "__main__":
    setup()
    app.run(host="0.0.0.0", port=5000)
