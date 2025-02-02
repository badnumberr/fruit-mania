import sqlite3

conn = sqlite3.connect('players.db')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS players;")

cursor.execute("""
CREATE TABLE players (
    nickname TEXT PRIMARY KEY,
    password TEXT,
    max_score INTEGER,
    registration_date TEXT
);
""")

conn.commit()
conn.close()