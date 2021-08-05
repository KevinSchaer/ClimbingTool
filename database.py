import sqlite3

connection = sqlite3.connect('climbing.db')
connection.row_factory = sqlite3.Row
db = connection.cursor()

db.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER,
        username TEXT NOT NULL UNIQUE,
        hash TEXT NOT NULL,
        bodyweight REAL,
        height INTEGER,
        age INTEGER,
        redpoint TEXT,
        onsight TEXT,
        about_me TEXT,
        profile TEXT DEFAULT "default.png",
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