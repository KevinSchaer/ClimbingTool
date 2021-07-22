import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

import sqlite3
from helpers import login_required

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# create connection to database
connection = sqlite3.connect('climbing.db', check_same_thread=False)
connection.row_factory = sqlite3.Row # allow to access return variable by column name
db = connection.cursor()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/enterRoute", methods=["GET", "POST"])
@login_required
def enterRoute():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        pass
    # if User reached route via GET
    else:
        return render_template("enterRoute.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    username = request.form.get("username")
    password = request.form.get("password")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not username:
            return render_template("error.html", error=["missing username"])

        # Ensure password was submitted
        elif not password:
            return render_template("error.html", error=["missing password"])

        # Query database for username
        db.execute("SELECT * FROM users WHERE username = :username", {"username": username})
        rows = db.fetchall()
        connection.commit()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return render_template("error.html", error=["invalid credentials"])

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not username:
            return render_template("error.html", error=["missing username"])

        # Ensure password was submitted
        elif not password:
            return render_template("error.html", error=["missing password"])

        # Ensure confirmation password was submitted
        elif not confirmation:
            return render_template("error.html", error=["missing confirmation"])

        # Ensure password and confirmation password are identical
        elif password != confirmation:
            return render_template("error.html", error=["different passwords"])

        # hash password
        hashPassword = generate_password_hash(password)

        try:
            db.execute("INSERT INTO users (username, hash) Values (:username, :hash)", {"username": username, "hash": hashPassword})
            connection.commit()
        except:
            return render_template("error.html", error=["user uniqueness"])

        # log them in
        rows = db.execute("SELECT id FROM users WHERE username = :username", {"username": username})
        rows = db.fetchall()
        connection.commit()
        if not rows:
            return render_template("error.html", error=["query failed"])

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/changePassword", methods=["GET", "POST"])
@login_required
def changePassword():
    """Change Password"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure password was submitted
        if not password:
            return render_template("error.html", error=["missing password"])

        # Ensure confirmation password was submitted
        elif not confirmation:
            return render_template("error.html", error=["missing confirmation"])

        # Ensure password and confirmation password are identical
        elif password != confirmation:
            return render_template("error.html", error=["different passwords"])

        # hash password
        hashPassword = generate_password_hash(password)

        # update password
        try:
            db.execute("UPDATE users SET hash = :hashPassword WHERE id = :user_id", {"hashPassword": hashPassword, "user_id": session["user_id"]})
            connection.commit()
        except:
            return render_template("error.html", error=["query failed"])

        flash('Password successfully changed!')

        # redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("changePassword.html")


if __name__ == "__main__":
    app.run()