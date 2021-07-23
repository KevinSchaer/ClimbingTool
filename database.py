import sqlite3

connection = sqlite3.connect('climbing.db')
connection.row_factory = sqlite3.Row
db = connection.cursor()

db.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER,
        username TEXT NOT NULL UNIQUE,
        hash TEXT NOT NULL,
        email TEXT NOT NULL,
        bodyweight REAL,
        height INTEGER,
        age INTEGER,
        redpoint TEXT,
        onsight TEXT,
        PRIMARY KEY (id)
    )""")

db.execute("""CREATE TABLE IF NOT EXISTS routes (
        id INTEGER,
        name TEXT NOT NULL,
        grade TEXT,
        spot TEXT,
        PRIMARY KEY (id)
    )""")

db.execute("""CREATE TABLE IF NOT EXISTS user_route (
        user_id INTEGER,
        route_id INTEGER,
        reached_top TEXT,
        attemps INTEGER,
        score INTEGER,
        user_grade TEXT,
        comment TEXT,
        PRIMARY KEY (user_id, route_id),
        FOREIGN KEY (user_id)
            REFERENCES users (id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION,
        FOREIGN KEY (route_id)
            REFERENCES routes (id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION
    )""")

def select():
    db.execute("SELECT * from users")
    connection.commit()
    rows = db.fetchall()
    print("There are {} entries".format(len(rows)))
    print(rows[0]["hash"])
    for row in rows:
        print(row["username"])

select()

db.execute("SELECT * from routes")
connection.commit()
rows = db.fetchall()
print(rows)

db.execute("SELECT * from user_route")
connection.commit()
rows = db.fetchall()
print(rows)