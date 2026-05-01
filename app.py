from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# ======================
# قاعدة البيانات
# ======================
def connect():
    return sqlite3.connect("students.db")

def create_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        course TEXT
    )
    """)

    conn.commit()
    conn.close()

# ======================
# HTML + CSS (واجهة جديدة)
# ======================
style = """
<style>
body{
    font-family: Arial;
    background:#0f172a;
    color:white;
    text-align:center;
    padding:20px;
}

.card{
    background:#1e293b;
    padding:20px;
    border-radius:12px;
    width:90%;
    margin:auto;
}

input{
    padding:10px;
    margin:5px;
    border:none;
    border-radius:8px;
    width:80%;
}

button{
    padding:10px 20px;
    background:#22c55e;
    border:none;
    border-radius:8px;
    color:white;
    cursor:pointer;
}

a{
    color:#38bdf8;
    text-decoration:none;
}

.student{
    background:#334155;
    margin:10px;
    padding:10px;
    border-radius:8px;
}
</style>
"""

home_page = style + """
<div class="card">
<h2>📚 نظام إدارة الطلاب</h2>

<form method="POST" action="/add">
    <input name="name" placeholder="اسم الطالب"><br>
    <input name="age" placeholder="العمر"><br>
    <input name="course" placeholder="التخصص"><br>
    <button>إضافة طالب</button>
</form>

<br>
<a href="/students">عرض الطلاب</a>
</div>
"""

students_page = style + """
<div class="card">
<h2>📋 قائمة الطلاب</h2>
<a href="/">رجوع</a>
<hr>

{% for s in students %}
<div class="student">
ID: {{s[0]}}<br>
الاسم: {{s[1]}}<br>
العمر: {{s[2]}}<br>
التخصص: {{s[3]}}
</div>
{% endfor %}
</div>
"""

# ======================
# الروابط
# ======================
@app.route("/")
def home():
    return render_template_string(home_page)

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    age = request.form["age"]
    course = request.form["course"]

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
                   (name, age, course))

    conn.commit()
    conn.close()

    return "<h3>✔️ تم إضافة الطالب</h3><a href='/'>رجوع</a>"

@app.route("/students")
def students():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()

    conn.close()

    return render_template_string(students_page, students=data)

# ======================
# تشغيل
# ======================
if __name__ == "__main__":
    create_table()
    app.run(host="0.0.0.0", port=5000)
