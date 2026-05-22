from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session
)

from flask_session import Session

from werkzeug.security import (
    check_password_hash
)

import sqlite3

app = Flask(__name__)

app.secret_key = "supersecretkey"

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)


@app.route("/")
def home():

    return render_template(
        "landing.html"
    )


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        conn = sqlite3.connect(
            "network_monitor.db"
        )

        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM users
            WHERE username = ?
        """, (username,))

        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(
            user[2],
            password
        ):

            session["user"] = username

            return redirect("/dashboard")

        else:

            return "Forkert brugernavn eller password"

    return render_template(
        "login.html"
    )


@app.route("/dashboard")
def dashboard():

    if "user" not in session:

        return redirect("/login")

    try:

        conn = sqlite3.connect(
            "network_monitor.db"
        )

        cursor = conn.cursor()

        cursor.execute("""

        SELECT
            devices.name,
            devices.ip_address,
            measurements.ping_ms,
            measurements.packet_loss,
            measurements.timestamp

        FROM measurements

        JOIN devices
        ON measurements.device_id = devices.id

        WHERE measurements.id IN (

            SELECT MAX(id)
            FROM measurements
            GROUP BY device_id

        )

        ORDER BY devices.name

        """)

        devices = cursor.fetchall()

        conn.close()

        return render_template(
            "dashboard.html",
            devices=devices
        )

    except Exception as e:

        return f"Database fejl: {e}"


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )