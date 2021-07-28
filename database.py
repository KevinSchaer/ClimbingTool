import sqlite3

connection = sqlite3.connect('climbing.db')
connection.row_factory = sqlite3.Row
db = connection.cursor()

db.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER,
        username TEXT NOT NULL UNIQUE,
        hash TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        bodyweight REAL,
        height INTEGER,
        age INTEGER,
        redpoint TEXT,
        onsight TEXT,
        about_me TEXT,
        PRIMARY KEY (id)
    );""")

db.execute("""CREATE TABLE IF NOT EXISTS routes (
        id INTEGER NOT NULL,
        name TEXT NOT NULL,
        grade TEXT NOT NULL,
        spot TEXT NOT NULL,
        PRIMARY KEY (id)
    );""")

db.execute("""CREATE TABLE IF NOT EXISTS user_route (
        user_id INTEGER,
        route_id INTEGER,
        top_reached TEXT,
        attempts INTEGER,
        score INTEGER,
        user_grade TEXT,
        comment TEXT,
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id, route_id),
        FOREIGN KEY (user_id)
            REFERENCES users (id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION,
        FOREIGN KEY (route_id)
            REFERENCES routes (id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION
    );""")

def select():
    db.execute("SELECT * from users")
    connection.commit()
    rows = db.fetchall()
    print("There are {} entries".format(len(rows)))
    print(rows[0]["hash"])
    for row in rows:
        print(row["username"])

#select()

#db.execute("INSERT INTO routes (name, grade, spot) Values (:name, :grade, :spot)", {"name": "Tschortschi", "grade": "6b", "spot": "Eppenberg"})
#connection.commit()

"""
db.execute("SELECT * FROM routes WHERE name = (:route_name) AND grade = (:grade) AND spot = (:spot)", {"route_name": "Tschortschi", "grade": "6b", "spot": "Eppenberg"})
routes = db.fetchall()
connection.commit()
print("There are {} entries".format(len(routes)))
print(routes[0]["id"])
print(routes[0]["name"])
print(routes[0]["grade"])
print(routes[0]["spot"])

#db.execute("INSERT INTO user_route (user_id, route_id, top_reached, attempts, score, user_grade, comment)", {"user_id": session["user_id"],"route_id": route_id, "top_reached": top_reached, "attempts": attempts, "score": score, "user_grade": user_grade, "comment": comment})
connection.commit()

print("_________________________")

db.execute("SELECT * from routes")
connection.commit()
rows = db.fetchall()
print(rows[1]["name"])

db.execute("SELECT * from user_route")
connection.commit()
rows = db.fetchall()
print(rows[0]["comment"])
if not rows:
    print("Hello")
else:
    print("Bye")
"""