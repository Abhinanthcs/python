import sqlite3
from flask import Flask, redirect, render_template_string, request, url_for

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect("admin.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    status_class = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        # Query database for matching username and password
        user = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password),
        ).fetchone()
        conn.close()

        if user:
            message = f"Welcome, {user['username']}! Login successful."
            status_class = "success"
        else:
            message = "Invalid username or password. Please try again."
            status_class = "error"

    html_template = """
    <!DOCTYPE html>
    <html>
    <body>
        <div class="login-card">
            <h2>Admin Login</h2>
            <form method="POST">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Log In</button>
            </form>

            {% if message %}
                <div class="message {{ status_class }}">
                    {{ message }}
                </div>
            {% endif %}
        </div>
    </body>
    </html>
    """

    return render_template_string(
        html_template, message=message, status_class=status_class
    )


if __name__ == "__main__":
    app.run(debug=True)