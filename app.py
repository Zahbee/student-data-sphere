from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# --- Initialize database ---
def init_db():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER,
                    gender TEXT,
                    dob TEXT,
                    email TEXT,
                    phone TEXT,
                    address TEXT,
                    major TEXT,
                    year TEXT,
                    gpa REAL,
                    enrollment_date TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

# --- Routes ---
@app.route("/")
def index():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    students = c.fetchall()
    conn.close()
    return render_template("index.html", students=students)

@app.route("/add", methods=["POST"])
def add():
    data = (
        request.form["name"],
        request.form["age"],
        request.form["gender"],
        request.form["dob"],
        request.form["email"],
        request.form["phone"],
        request.form["address"],
        request.form["major"],
        request.form["year"],
        request.form["gpa"],
        request.form["enrollment_date"]
    )
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("INSERT INTO students (name, age, gender, dob, email, phone, address, major, year, gpa, enrollment_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    data = (
        request.form["name"],
        request.form["age"],
        request.form["gender"],
        request.form["dob"],
        request.form["email"],
        request.form["phone"],
        request.form["address"],
        request.form["major"],
        request.form["year"],
        request.form["gpa"],
        request.form["enrollment_date"],
        id
    )
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("""UPDATE students SET
                 name=?, age=?, gender=?, dob=?, email=?, phone=?, address=?,
                 major=?, year=?, gpa=?, enrollment_date=? WHERE id=?""", data)
    conn.commit()
    conn.close()
    return redirect("/")


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)










