from flask import Flask, render_template, request, redirect, session
import joblib
import mysql.connector
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # for session management

# Load sentiment model
model = joblib.load('C:/Users/sande/Downloads/flask/sentiment_analysis/sentiment_model.pkl')


# Connect to XAMPP MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",         # default XAMPP password is blank
    database="sentiment_analysis"
)
cursor = db.cursor()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        user_text = request.form['text'].strip().lower()
        user_text = re.sub(r'[^a-zA-Z\s]', '', user_text)
        sentiment = model.predict([user_text])[0]

        # Save to DB
        cursor.execute("INSERT INTO user_inputs (username, user_text, sentiment) VALUES (%s, %s, %s)",
                       (username, user_text, sentiment))
        db.commit()

        return render_template('index.html', sentiment=sentiment)
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        passwd = request.form['password']
        cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (uname, passwd))
        result = cursor.fetchone()
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
    cursor.execute("SELECT * FROM user_inputs ORDER BY timestamp DESC")
    records = cursor.fetchall()
    return render_template('admin.html', records=records)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
  # Localhost
