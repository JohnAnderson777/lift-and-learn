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
    return render_template("index.html")


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

