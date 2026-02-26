from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret123"

# ---------- DATABASE ----------
DB_NAME = "users.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT,
            phone TEXT,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

create_table()

# ---------- ROUTES ----------
@app.route("/")
def home():
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]

        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, email, phone, password) VALUES (?, ?, ?, ?)",
                (username, email, phone, password)
            )
            conn.commit()
            conn.close()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("home"))
        except sqlite3.IntegrityError:
            flash("Username already exists!", "error")
            return redirect(url_for("register"))

    return render_template("register.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        return "✅ Login successful"
    else:
        flash("Invalid username or password", "error")
        return redirect(url_for("home"))

# ---------- RUN APP (RENDER FIX) ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
