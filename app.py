from flask import Flask, render_template, request, redirect, session
import joblib
import sqlite3
import re
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # for session management

# Load sentiment model
model = joblib.load('predict.pkl')

# Database setup
DB_NAME = 'sentiment.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_inputs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            user_text TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    # Insert default admin if not exists
    c.execute("SELECT * FROM admin WHERE username='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO admin (username, password) VALUES (?, ?)", ("sandeep", "sandeep17"))
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        user_text = request.form['text'].strip().lower()
        user_text = re.sub(r'[^a-zA-Z\s]', '', user_text)
        sentiment = model.predict([user_text])[0]

        # Save to DB
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO user_inputs (username, user_text, sentiment) VALUES (?, ?, ?)",
                  (username, user_text, sentiment))
        conn.commit()
        conn.close()

        return render_template('index.html', sentiment=sentiment)
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        passwd = request.form['password']
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM admin WHERE username=? AND password=?", (uname, passwd))
        result = c.fetchone()
        conn.close()
        if result:
            session['admin'] = uname
            return redirect('/admin')
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/admin')
def admin():
    if 'admin' not in session:
        return redirect('/login')
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM user_inputs ORDER BY timestamp DESC")
    records = c.fetchall()
    conn.close()
    return render_template('admin.html', records=records)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/login')

init_db()

if __name__ == '__main__':
      # Ensure database and tables are created
    app.run(debug=True)
