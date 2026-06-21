from flask import Flask, request, render_template, g
import sqlite3
import os

app = Flask(__name__)
FLAG = os.environ.get('FLAG') or 'HL4{placeholder_flag_here}'
DB_PATH = '/tmp/portal.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
    return db


@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS employees')
    c.execute('''CREATE TABLE employees (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )''')
    c.execute("INSERT INTO employees VALUES (1, 'admin', 'Tr0ub4dor&3', 'admin')")
    c.execute("INSERT INTO employees VALUES (2, 'alice', 'alice2024!', 'staff')")
    c.execute("INSERT INTO employees VALUES (3, 'bob', 'b0bRules99', 'staff')")
    conn.commit()
    conn.close()


with app.app_context():
    init_db()


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        try:
            db = get_db()
            c = db.cursor()
            # Vulnerable query — do NOT use in production
            query = f"SELECT * FROM employees WHERE username='{username}' AND password='{password}'"
            c.execute(query)
            user = c.fetchone()
            if user:
                return render_template('dashboard.html', username=user[1], role=user[3], flag=FLAG)
            error = 'Invalid credentials.'
        except Exception as e:
            error = f'Database error: {e}'
    return render_template('login.html', error=error)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
