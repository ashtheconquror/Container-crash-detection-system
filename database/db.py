# SQLite connection

import sqlite3

DB_PATH = "database/events.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    with open("database/schema.sql", "r") as f:
        # Filter out comment lines and empty lines, then execute
        sql_script = "\n".join(
            line for line in f.read().split("\n")
            if line.strip() and not line.strip().startswith("--")
        )
        conn.executescript(sql_script)
    conn.commit()
    conn.close()
