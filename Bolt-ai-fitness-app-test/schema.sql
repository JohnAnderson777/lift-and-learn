-- !sqlitedb
-- Fitness Workout Plan Website Database Schema
-- SQLite Database for A-Level Computer Science NEA

-- Users table for authentication
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User profiles table storing fitness information
CREATE TABLE IF NOT EXISTS user_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    age INTEGER NOT NULL CHECK (age > 0 AND age < 120),
    weight REAL NOT NULL CHECK (weight > 0),
    height REAL NOT NULL CHECK (height > 0),
    fitness_type TEXT NOT NULL CHECK (fitness_type IN ('general_fitness', 'athlete', 'muscle_strength', 'calisthenics')),
    fitness_level TEXT NOT NULL CHECK (fitness_level IN ('beginner', 'intermediate', 'advanced')),
    goals TEXT NOT NULL,
    workout_days INTEGER NOT NULL CHECK (workout_days >= 1 AND workout_days <= 7),
    session_duration INTEGER NOT NULL CHECK (session_duration > 0),
    medical_conditions TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Workout plans table
CREATE TABLE IF NOT EXISTS workout_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    plan_name TEXT NOT NULL,
    fitness_type TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    plan_data TEXT NOT NULL,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_workout_plans_user_id ON workout_plans(user_id);
CREATE INDEX IF NOT EXISTS idx_workout_plans_is_active ON workout_plans(user_id, is_active);
