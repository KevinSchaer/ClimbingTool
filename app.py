import os
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask.helpers import url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

import sqlite3
from helpers import login_required

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['JSON_SORT_KEYS'] = False

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

# Fixed values
GRADES = []
USER_GRADES = []
TOP_REACHED = ["Yes", "No"]
SCORES = [1, 2, 3, 4, 5]

for number in range(4,7):
    for letter in ["a", "b", "c"]:
        for symbol in ["", "+"]:
            GRADES.append(str(number)+letter+symbol)
            USER_GRADES.append(str(number)+letter+symbol)



@app.route("/editRoute", methods=["GET", "POST"])
@login_required
def editRoute():
    user_id = session["user_id"]
    db.execute("SELECT DISTINCT spot FROM user_route INNER JOIN routes ON user_route.route_id = routes.id  WHERE user_id = :user_id ORDER BY time DESC;", {"user_id": user_id})
    result_spot = db.fetchall()
    """
    db.execute("SELECT name FROM routes WHERE spot = :spot ORDER BY name DESC;", {"spot": result_spot[0]["spot"]})
    result_names = db.fetchall()
    connection.commit()
    names = []
    """
    spots = []
    for i in range(0,len(result_spot)):
        spots.append(result_spot[i]["spot"])
    """
    for i in range(0,len(result_names)):
        names.append(result_names[i]["name"])    
    """
    if request.method == "POST":
        return "<h1>Spot: {}, Name: {}</h1>".format(request.form.get("spot"), request.form.get("name"))


    return render_template("editRoute.html", names=[], spots=spots, grades=GRADES, user_grades=USER_GRADES, top_reached=TOP_REACHED, scores=SCORES)

@app.route("/editRoute/<spot>")
@login_required
def name(spot):
    """
    helper function for editRoute(), used by javascript in editRoute.html
    """
    db.execute("SELECT DISTINCT name FROM routes WHERE spot = :spot ORDER BY name DESC;", {"spot": spot})
    result_names = db.fetchall()
    connection.commit()
    nameArray = []
    for i in range(0,len(result_names)):
        nameObj = {}
        nameObj["name"] = result_names[i]["name"]
        nameArray.append(nameObj)

    return jsonify({"names": nameArray})


@app.route("/processRouteEditInput", methods=["POST"])
@login_required
def processRouteEditInput():
    user_id = session["user_id"]
    name = request.form["name"]
    spot = request.form["spot"]

    #
    #
    # ADD TRY CATCH + ERROR MESSAGE / HANDLING
    #
    #

    db.execute("SELECT grade, user_grade, attempts, top_reached, score, comment FROM user_route INNER JOIN routes ON user_route.route_id = routes.id  WHERE user_id = :user_id AND name = :name AND spot = :spot;", {"user_id": user_id, "name": name, "spot": spot})

    result = db.fetchall()
    connection.commit()

    if result:
        return jsonify([dict(row) for row in result])
    else:
        return jsonify({"error": "Missing data!"})


@app.route("/searchRoutes", methods=["GET","POST"])
@login_required
def searchRoutes():
    user_id = session["user_id"]
    if request.method == "POST":
        """
        allow user to search routes climbed by spot, grade, score or all possible combinations
        """
        spot = request.form.get("spot")
        if not spot:
            spot = None # change empty string to None
        grade = request.form.get("grade")
        score = request.form.get("score")
        db.execute("SELECT top_reached, attempts, score, user_grade, comment, name, grade, spot FROM user_route INNER JOIN routes ON user_route.route_id = routes.id  WHERE user_id = :user_id AND spot = CASE WHEN :spot COLLATE NOCASE IS NULL THEN spot ELSE :spot COLLATE NOCASE END AND grade = CASE WHEN :grade IS NULL THEN grade ELSE :grade END AND score = CASE WHEN :score IS NULL THEN score ELSE :score END ORDER BY time DESC;", {"user_id": user_id, "spot": spot, "grade": grade, "score": score})
        result_routes = db.fetchall()
        connection.commit()
        # show template with the filtered routes
        return render_template("searchRoutes.html", result_routes=result_routes, grades=GRADES, scores=SCORES)
    else:
        # show all routes of the user
        db.execute("SELECT top_reached, attempts, score, user_grade, comment, name, grade, spot FROM user_route INNER JOIN routes ON user_route.route_id = routes.id  WHERE user_id = :user_id ORDER BY time DESC;", {"user_id": user_id})
        result_routes = db.fetchall()
        connection.commit()
        return render_template("searchRoutes.html", result_routes=result_routes, grades=GRADES, scores=SCORES)


@app.route("/deleteUser", methods=["GET","POST"])
@login_required
def deleteUser():
    if request.method == "POST":
        """
        delete account of user which is currently logged in
        """
        user_id = session["user_id"]
        # ON DELETE CASCADE does only work in SQLITE extension but not in flask - I don't know why
        db.execute("PRAGMA foreign_keys = ON")
        db.execute("DELETE FROM users WHERE id = :user_id", {"user_id": user_id})
        connection.commit()
        session.clear()
        flash("You have successfully deleted your Account") # is not shown
        return redirect("/")
    else:
        return render_template("deleteUser.html")


@app.route("/")
@login_required
def index():

    user_id = session["user_id"]
    # Get existing user values from database
    db.execute("SELECT * FROM users WHERE id = :user_id", {"user_id": user_id})
    result_users = db.fetchone()
    # Get route data from current user from database
    db.execute("SELECT top_reached, attempts, score, user_grade, comment, name, grade, spot FROM user_route INNER JOIN routes ON user_route.route_id = routes.id  WHERE user_id = :user_id ORDER BY time DESC;", {"user_id": user_id})
    result_routes = db.fetchall()
    # get number of routes per grade climbed for current user from database
    db.execute("SELECT grade, COUNT(*) AS COUNT FROM routes INNER JOIN user_route ON user_route.route_id = routes.id  WHERE user_id = :user_id GROUP BY grade", {"user_id": user_id})
    route_data = db.fetchall()
    connection.commit()
    # create separate list for values (COUNT) and labels (grade)
    labels = []
    values = []
    for i in range(0,len(route_data)):
        labels.append(route_data[i]["grade"])
        values.append(route_data[i]["COUNT"])

    return render_template("index.html", result_users=result_users, result_routes=result_routes, labels=labels, values=values)


@app.route("/editUserProfile", methods=["GET", "POST"])
@login_required
def editUserProfile():

    user_id = session["user_id"]

    # Get existing user values from database
    db.execute("SELECT * FROM users WHERE id = :user_id", {"user_id": user_id})
    result = db.fetchone()
    connection.commit()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        age = request.form.get("age")
        height = request.form.get("height")
        bodyweight = request.form.get("bodyweight")
        redpoint = request.form.get("redpoint")
        onsight = request.form.get("onsight")
        about_me = request.form.get("about_me")
        
        if not age:
            age = result["age"]
        else:
            # Check if the form input is an integer 
            try:
                age = int(age)
                if age <= 0:
                    return render_template("error.html", error=["invalid value"])
            except:
                return render_template("error.html", error=["invalid value"])

        if not height:
            height = result["height"]
        else:
            # Check if the form input is an integer 
            try:
                height = int(height)
                if height <= 0:
                    return render_template("error.html", error=["invalid value"])
            except:
                return render_template("error.html", error=["invalid value"])

        if not bodyweight:
            bodyweight = result["bodyweight"]
        else:
            # Check if the form input is a float
            try:
                bodyweight = float(bodyweight)
                if bodyweight <= 0:
                    return render_template("error.html", error=["invalid value"])
            except:
                return render_template("error.html", error=["invalid value"])

        if not redpoint:
            redpoint = result["redpoint"]
        else:
            # Check for valid values from select-options
            if redpoint not in GRADES:
                return render_template("error.html", error=["invalid value"])

        if not onsight:
            onsight = result["onsight"]
        else:
            # Check for valid values from select-options
            if onsight not in GRADES:
                return render_template("error.html", error=["invalid value"])
        
        if not about_me:
            about_me = result["about_me"]
        
        try:
            db.execute("UPDATE users SET age = :age, height = :height, bodyweight = :bodyweight, redpoint = :redpoint, onsight = :onsight, about_me = :about_me WHERE id = :user_id", {"age": age, "height": height, "bodyweight": bodyweight, "redpoint": redpoint, "onsight": onsight, "about_me": about_me, "user_id": user_id})
            connection.commit()
        except:
            return render_template("error.html", error=["query failed"])
        
        flash('You have successfully updated your user profile!')

        return redirect("/editUserProfile")

    # if User reached route via GET
    else:
        return render_template("editUserProfile.html", grades=GRADES, result=result)


@app.route("/searchUser")
@login_required
def searchUser():
    return render_template("searchUser.html")


@app.route("/search")
@login_required
def search():
    q = request.args.get("q")
    if q:
        db.execute("SELECT username FROM users WHERE username LIKE ?", ("%" + q + "%",))
        result = db.fetchall()
        connection.commit()
    else:
        result = []
    return jsonify([dict(row) for row in result])


@app.route("/enterRoute", methods=["GET", "POST"])
@login_required
def enterRoute():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        route_name = request.form.get("route_name")
        spot = request.form.get("spot")
        grade = request.form.get("grade")
        user_grade = request.form.get("user_grade")
        attempts = request.form.get("attempts")
        top_reached = request.form.get("top_reached")
        comment = request.form.get("comments")
        score = request.form.get("score")
        
        # Check if the form is completed; comments are voluntarily
        if not route_name:
            return render_template("error.html", error=["incomplete form"])
        
        if not spot:
            return render_template("error.html", error=["incomplete form"])
        
        if not grade:
            return render_template("error.html", error=["incomplete form"])
        
        if not user_grade:
            return render_template("error.html", error=["incomplete form"])

        if not attempts:
            return render_template("error.html", error=["incomplete form"])

        if not top_reached:
            return render_template("error.html", error=["incomplete form"])

        if not score:
            return render_template("error.html", error=["incomplete form"])
        
        # convert attempts and score to an integer
        try:
            attempts = int(attempts)
            score = int(score)
        except:
            return render_template("error.html", error=["invalid value"])

        # Check for positive values (attempt input)
        if  attempts <= 0:
            return render_template("error.html", error=["invalid value"])
        
        # Check for valid values from select-options
        if grade not in GRADES:
            return render_template("error.html", error=["invalid value"])

        if user_grade not in USER_GRADES:
            return render_template("error.html", error=["invalid value"])
        
        if top_reached not in TOP_REACHED:
            return render_template("error.html", error=["invalid value"])
        
        if score not in SCORES:
            return render_template("error.html", error=["invalid value"])
        
        # database queries
        try:
            db.execute("SELECT id FROM routes WHERE name = (:route_name) AND grade = (:grade) AND spot = (:spot)", {"route_name": route_name, "grade": grade, "spot": spot})
            route = db.fetchall()
            connection.commit()
        except:
            return render_template("error.html", error=["query failed"])

        if not route:
            try:
                db.execute("INSERT INTO routes (name, grade, spot) Values (:route_name, :grade, :spot)", {"route_name": route_name, "grade": grade, "spot": spot})
                db.execute("SELECT id FROM routes WHERE name = (:route_name) AND grade = (:grade) AND spot = (:spot)", {"route_name": route_name, "grade": grade, "spot": spot})
                route = db.fetchall()
                connection.commit()
            except:
                return render_template("error.html", error=["query failed"])

        route_id = route[0]["id"]

        try:
            db.execute("INSERT INTO user_route (user_id, route_id, top_reached, attempts, score, user_grade, comment) VALUES (:user_id, :route_id, :top_reached, :attempts, :score, :user_grade, :comment)", {"user_id": session["user_id"],"route_id": route_id, "top_reached": top_reached, "attempts": attempts, "score": score, "user_grade": user_grade, "comment": comment})
            connection.commit()
        except:
            return render_template("error.html", error=["query failed"])

        flash('You have successfully entered a new route!')

        return redirect("/enterRoute")

    # if User reached route via GET
    else:
        return render_template("enterRoute.html", grades=GRADES, user_grades=USER_GRADES, top_reached=TOP_REACHED, scores=SCORES)


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
    email = request.form.get("email")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not username:
            return render_template("error.html", error=["missing username"])
            
        # Ensure email was submitted
        if not email:
            return render_template("error.html", error=["missing email"])

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
            db.execute("INSERT INTO users (username, hash, email) Values (:username, :hash, :email)", {"username": username, "hash": hashPassword, "email": email})
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
    app.run(debug=True)