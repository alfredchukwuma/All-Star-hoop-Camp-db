import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

def init_db():
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fname TEXT,
            lname TEXT,
            age INTEGER,
            race TEXT,
            email TEXT,
            phone_number TEXT,
            address TEXT,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = c.fetchone()
        conn.close()
        
        if user:
            stored_password = user[8]  # assuming password is the 9th field in the table
            if check_password_hash(stored_password, password):
                flash('You have successfully logged in!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Incorrect password, please try again.', 'danger')
        else:
            flash('User not found, please check your email.', 'danger')
            
    return render_template('login.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    age = request.form.get('age')
    race = request.form.get('Race')
    email = request.form.get('Email')
    phone_number = request.form.get('phone_number')
    address = request.form.get('address')
    password = request.form.get('Password')

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO users (fname, lname, age, race, email, phone_number, address, password)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (fname, lname, age, race, email, phone_number, address, hashed_password))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

@app.route('/view_data')
def view_data():
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    rows = c.fetchall()
    conn.close()
    return render_template('view_data.html', rows=rows)

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)

