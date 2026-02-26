from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

DB_NAME = "users.db"

# ---------- LOGIN PAGE ----------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cur.fetchone()
        conn.close()

        if user:
            return "Login Successful"
        else:
            return "Invalid Credentials"

    return render_template("login.html")


# ---------- VIEW USERS IN BROWSER ----------
@app.route("/users")
def view_users():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT id, username, email, phone FROM users")
    users = cur.fetchall()

    conn.close()

    return f"""
    <h2>Registered Users</h2>
    <table border="1" cellpadding="8">
        <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Email</th>
            <th>Phone</th>
        </tr>
        {''.join([f"<tr><td>{u[0]}</td><td>{u[1]}</td><td>{u[2]}</td><td>{u[3]}</td></tr>" for u in users])}
    </table>
    """

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")