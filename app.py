from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3, os

app = Flask(__name__)
app.secret_key = "supersecretkey"

DB_NAME = "dating.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        age INTEGER,
        bio TEXT
    )""")
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        age = request.form["age"]
        bio = request.form["bio"]
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username,password,age,bio) VALUES (?,?,?,?)",
                      (username,password,age,bio))
            conn.commit()
        except:
            conn.close()
            return "Username already exists!"
        conn.close()
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?",(username,password))
        user = c.fetchone()
        conn.close()
        if user:
            session["user"] = user[1]
            return redirect(url_for("profile"))
        return "Invalid login!"
    return render_template("login.html")

@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect(url_for("login"))
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT username,age,bio FROM users WHERE username=?",(session["user"],))
    user = c.fetchone()
    conn.close()
    return render_template("profile.html", user=user)

@app.route("/browse")
def browse():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT username,age,bio FROM users")
    users = c.fetchall()
    conn.close()
    return render_template("browse.html", users=users)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)