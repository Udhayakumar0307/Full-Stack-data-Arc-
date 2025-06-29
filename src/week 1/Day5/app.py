from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            dept TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('register.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    dept = request.form['dept']
    phone = request.form['phone']

    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("INSERT INTO students (name, email, dept, phone) VALUES (?, ?, ?, ?)",
              (name, email, dept, phone))
    conn.commit()
    conn.close()
    return redirect('/students')

@app.route('/students')
def students():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    all_students = c.fetchall()
    conn.close()
    return render_template('students.html', students=all_students)

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/students')

@app.route('/edit/<int:id>')
def edit(id):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students WHERE id=?", (id,))
    student = c.fetchone()
    conn.close()
    return render_template('edit.html', student=student)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    name = request.form['name']
    email = request.form['email']
    dept = request.form['dept']
    phone = request.form['phone']
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("UPDATE students SET name=?, email=?, dept=?, phone=? WHERE id=?",
              (name, email, dept, phone, id))
    conn.commit()
    conn.close()
    return redirect('/students')

if __name__ == '__main__':
    app.run(debug=True)
