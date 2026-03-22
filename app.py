from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import re
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
    )

# -------------------------
# LOGIN
# -------------------------
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM accounts WHERE username = %s", (username,))
        account = cursor.fetchone()

        if account and check_password_hash(account['password'], password):
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('index'))
        else:
            msg = 'Incorrect username or password!'

    return render_template('login.html', msg=msg)

# -------------------------
# INDEX
# -------------------------
@app.route('/index')
def index():
    if 'loggedin' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

# -------------------------
# LOGOUT
# -------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# -------------------------
# REGISTER
# -------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']
        email = request.form['email']

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM accounts WHERE username = %s", (username,))
        account = cursor.fetchone()

        cursor.execute("SELECT * FROM accounts WHERE email = %s", (email,))
        email_exists = cursor.fetchone()

        if account:
            msg = 'Username already exists!'
        elif email_exists:
            msg = 'Email already registered!'
        elif password != confirm:
            msg = 'Passwords do not match!'
        else:
            hashed_password = generate_password_hash(password)
            cursor.execute(
                "INSERT INTO accounts (username, password, email) VALUES (%s, %s, %s)",
                (username, hashed_password, email)
            )
            db.commit()
            msg = 'Registration successful!'

    return render_template('register.html', msg=msg)

# -------------------------
# ACCESSIBILITY SETTINGS
# -------------------------
@app.route('/settings/accessibility')
def accessibility_settings():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM accessibility WHERE user_id = %s", (session['id'],))
    settings = cursor.fetchone()

    if not settings:
        cursor.execute("INSERT INTO accessibility (user_id) VALUES (%s)", (session['id'],))
        db.commit()
        cursor.execute("SELECT * FROM accessibility WHERE user_id = %s", (session['id'],))
        settings = cursor.fetchone()

    return render_template('accessibility.html', settings=settings)


@app.route('/settings/accessibility/update', methods=['POST'])
def update_accessibility():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    data = request.json

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE accessibility
        SET text_size=%s, icon_size=%s, tts=%s, autoscroll=%s,
            dark_mode=%s, colour_filter=%s, language=%s
        WHERE user_id=%s
    """, (
        data['text_size'],
        data['icon_size'],
        data['tts'],
        data['autoscroll'],
        data['dark_mode'],
        data['colour_filter'],
        data['language'],
        session['id']
    ))

    db.commit()
    return {"status": "ok"}

# -------------------------
# SERVER START (LAST LINE)
from waitress import serve

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)
