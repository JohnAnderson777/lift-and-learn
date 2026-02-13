from multiprocessing.util import debug
from pdb import run
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3


app = Flask(__name__)


app.secret_key = "i_Love_OCR"
app.permanent_session_lifetime = timedelta(hours=5)

@app.route("/")
def home():
    return render_template("dashboard.html")


@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]    
        return f"<h1>{user}</h1>"
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/contact")
def contact():
    return render_template("contact.html")



@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']   
        hashedPassword = generate_password_hash(password, method='pbkdf2:sha256')

        conn = DatabaseConnect()
        try:
        # ? placeholders to stop SQL injection
            conn.execute('INSERT INTO users (username, hash, email) VALUES (?, ?, ?)', (username, hashedPassword, email))
            conn.commit()
            conn.close()
            flash("Registration successful. Now please Login to your account.")
            return redirect(url_for('login'))


   # If username already taken:

        except sqlite3.IntegrityError:
            flash("Username already exists. Please choose a different username.")
            return redirect(url_for('register'))

    return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']


     # Fetch user data

        conn = DatabaseConnect()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

    # check user exists + hashed password matches

        if user and check_password_hash(user['hashedPassword'], password):
            session['user.id'] = user['id']
            session['username'] = user['username']
            session['password'] = user['password']
            return redirect(url_for('user'))
        else:
            flash("Invalid username or password. Please try again.")
            return redirect(url_for('login'))
        
    return render_template("login.html")




# -/////   DATABASE   //////


def DatabaseConnect():
    conn = sqlite3.connect("./SQLite/Fitness Database.db")
    conn.row_factory = sqlite3.Row
    print("Database Connected Successfully")
    return conn



if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from database import init_db, User, UserProfile, WorkoutPlan
from workout_generator import generate_workout_plan
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Please provide both email and password', 'error')
            return render_template('register.html')

        user_id = User.create(email, password)
        if user_id:
            user = User.get_by_email(email)
            login_user(user)
            return redirect(url_for('questionnaire'))
        else:
            flash('Email already exists. Please login instead.', 'error')
            return render_template('register.html')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.get_by_email(email)

        if user and user.check_password(password):
            login_user(user)
            profile = UserProfile.get_by_user_id(user.id)
            if profile:
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('questionnaire'))
        else:
            flash('Invalid email or password', 'error')
            return render_template('login.html')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/questionnaire', methods=['GET', 'POST'])
@login_required
def questionnaire():
    profile = UserProfile.get_by_user_id(current_user.id)
    if profile:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        data = {
            'full_name': request.form.get('full_name'),
            'age': int(request.form.get('age')),
            'weight': float(request.form.get('weight')),
            'height': float(request.form.get('height')),
            'fitness_type': request.form.get('fitness_type'),
            'fitness_level': request.form.get('fitness_level'),
            'goals': request.form.get('goals'),
            'workout_days': int(request.form.get('workout_days')),
            'session_duration': int(request.form.get('session_duration')),
            'medical_conditions': request.form.get('medical_conditions', '')
        }

        if UserProfile.create(current_user.id, data):
            workout_plan_data = generate_workout_plan({
                'fitness_type': data['fitness_type'],
                'fitness_level': data['fitness_level'],
                'workout_days': data['workout_days'],
                'session_duration': data['session_duration'],
                'goals': data['goals']
            })

            plan_name = f"{data['fitness_type'].replace('_', ' ').title()} {data['fitness_level'].title()} Plan"

            WorkoutPlan.create(
                current_user.id,
                plan_name,
                data['fitness_type'],
                data['fitness_level'],
                workout_plan_data
            )

            return redirect(url_for('dashboard'))
        else:
            flash('Error creating profile. Please try again.', 'error')

    return render_template('questionnaire.html')

@app.route('/dashboard')
@login_required
def dashboard():
    profile = UserProfile.get_by_user_id(current_user.id)
    if not profile:
        return redirect(url_for('questionnaire'))

    workout_plan = WorkoutPlan.get_active_by_user_id(current_user.id)

    return render_template('dashboard.html', profile=profile, workout_plan=workout_plan, user=current_user)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)import sqlite3
import json
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

DATABASE = 'fitness_app.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    with open('schema.sql', 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

class User:
    def __init__(self, id, email, password_hash, created_at):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return str(self.id)

    @staticmethod
    def create(email, password):
        conn = get_db()
        password_hash = generate_password_hash(password)
        try:
            cursor = conn.execute(
                'INSERT INTO users (email, password_hash) VALUES (?, ?)',
                (email, password_hash)
            )
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            conn.close()
            return None

    @staticmethod
    def get_by_email(email):
        conn = get_db()
        user_data = conn.execute(
            'SELECT * FROM users WHERE email = ?', (email,)
        ).fetchone()
        conn.close()
        if user_data:
            return User(user_data['id'], user_data['email'],
                       user_data['password_hash'], user_data['created_at'])
        return None

    @staticmethod
    def get_by_id(user_id):
        conn = get_db()
        user_data = conn.execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()
        conn.close()
        if user_data:
            return User(user_data['id'], user_data['email'],
                       user_data['password_hash'], user_data['created_at'])
        return None

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class UserProfile:
    @staticmethod
    def create(user_id, data):
        conn = get_db()
        try:
            conn.execute('''
                INSERT INTO user_profiles
                (user_id, full_name, age, weight, height, fitness_type,
                 fitness_level, goals, workout_days, session_duration, medical_conditions)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, data['full_name'], data['age'], data['weight'],
                  data['height'], data['fitness_type'], data['fitness_level'],
                  data['goals'], data['workout_days'], data['session_duration'],
                  data.get('medical_conditions', '')))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            print(f"Error creating profile: {e}")
            return False

    @staticmethod
    def get_by_user_id(user_id):
        conn = get_db()
        profile = conn.execute(
            'SELECT * FROM user_profiles WHERE user_id = ?', (user_id,)
        ).fetchone()
        conn.close()
        return dict(profile) if profile else None

class WorkoutPlan:
    @staticmethod
    def create(user_id, plan_name, fitness_type, difficulty, plan_data):
        conn = get_db()
        try:
            conn.execute('''
                INSERT INTO workout_plans
                (user_id, plan_name, fitness_type, difficulty, plan_data, is_active)
                VALUES (?, ?, ?, ?, ?, 1)
            ''', (user_id, plan_name, fitness_type, difficulty, json.dumps(plan_data)))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            print(f"Error creating workout plan: {e}")
            return False

    @staticmethod
    def getn = get_db()
        plan = conn.execute(
            'SELECT * FROM workout_plans WHERE user_id = ? AND is_active = 1 ORDER BY created_at DESC LIMIT 1',
            (user_id,)
        ).fetchone()
        conn.close()
        if plan:
            plan_dict = dict(plan)
            plan_dict['plan_data'] = json.loads(plan_dict['plan_data'])
            return plan_dict
        return None_active_by_user_id(user_id):
        con