from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from database import init_db, User, UserProfile, WorkoutPlan
from workout_generator import generate_workout_plan
import os


app = Flask(__name__)
app.secret_key = "I_Love_OCR"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

@app.template_filter('get_user_profile')
def get_user_profile(user_id):
    return UserProfile.get_by_user_id(user_id)

@app.template_filter('get_workout_plan')
def get_workout_plan(user_id):
    return WorkoutPlan.get_active_by_user_id(user_id)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

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
            return redirect(url_for('index'))
        else:
            flash('Email already exists. Please login instead.', 'error')
            return render_template('register.html')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.get_by_email(email)

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'error')
            return render_template('login.html')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    if not current_user.is_authenticated:
        session['questionnaire_data'] = None
        flash('Please login or register to save your workout plan', 'info')
        return redirect(url_for('login'))

    profile = UserProfile.get_by_user_id(current_user.id)
    if profile:
        return redirect(url_for('index'))

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

            return redirect(url_for('index'))
        else:
            flash('Error creating profile. Please try again.', 'error')

    return render_template('questionnaire.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
