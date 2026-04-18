from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY, name TEXT)')
    conn.commit()
    conn.close()

def get_employees():
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    c.execute('SELECT name FROM employees')
    data = [row[0] for row in c.fetchall()]
    conn.close()
    return data

@app.route('/')
def home():
    employees = get_employees()
    return render_template_string("""
    <html>
    <head>
        <title>Employee Directory</title>
        <style>
             body { font-family: Arial; background: #eef2f7; text-align: center; }
            .container {
                width: 400px; margin: 60px auto; background: white;
                padding: 25px; border-radius: 10px;
                box-shadow: 0 0 12px rgba(0,0,0,0.1);
            }
            input {
                padding: 10px; width: 65%;
                border-radius: 5px; border: 1px solid #ccc;
            }
            button {
                padding: 10px; background: blue; color: white;
                border: none; border-radius: 5px;
            }
            li {
                background: #f1f2f6;
                margin: 5px; padding: 10px; border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Employee Directory</h2>

            <form method="POST" action="/add">
                <input type="text" name="name" placeholder="Enter name..." required>
                <button type="submit">Add Employee</button>
            </form>

            <h3>Employee List</h3>
            <ul>
                {% for emp in employees %}
                    <li>{{ emp }}</li>
                {% endfor %}
            </ul>
        </div>
    </body>
    </html>
    """, employees=employees)

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name')
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    c.execute('INSERT INTO employees (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()
    return home()

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
