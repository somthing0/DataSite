from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask application
app = Flask(__name__)
app.secret_key = "6924[j)zm>;%?(C4dyh~,dj<%"

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Load user function
@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        return User(*user_data)
    return None

# Database initialization function
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Home route
@app.route('/')
@app.route('/dashboard')
@login_required
def home():
    return render_template("index.html")

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template("register.html")
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        if cursor.fetchone():
            flash('Username already exists', 'error')
            conn.close()
            return render_template("register.html")
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, generate_password_hash(password)))
        conn.commit()
        conn.close()
        flash('Registration successful', 'success')
        return redirect(url_for('login'))
    return render_template("register.html")

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user_data = cursor.fetchone()
        conn.close()
        if user_data and check_password_hash(user_data[2], password):
            user = User(*user_data)
            login_user(user)
            flash('Login successful', 'success')
            return redirect(url_for('home'))
        flash('Invalid username or password', 'error')
    return render_template("login.html")

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful', 'success')
    return redirect(url_for('login'))

# Initialize the database and run the application
if __name__ == "__main__":
    init_db()  # Create the database and users table if it doesn't exist
    app.run(debug=True, host="0.0.0.0")
