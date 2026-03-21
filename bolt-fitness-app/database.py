import sqlite3
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
    def get_active_by_user_id(user_id):
        conn = get_db()
        plan = conn.execute(
            'SELECT * FROM workout_plans WHERE user_id = ? AND is_active = 1 ORDER BY created_at DESC LIMIT 1',
            (user_id,)
        ).fetchone()
        conn.close()
        if plan:
            plan_dict = dict(plan)
            plan_dict['plan_data'] = json.loads(plan_dict['plan_data'])
            return plan_dict
        return None
