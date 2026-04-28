import sqlite3

DB = "jwks.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password_hash TEXT,
        email TEXT,
        date_registered TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS auth_logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        request_ip TEXT NOT NULL,
        request_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        user_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS keys(
        kid INTEGER PRIMARY KEY AUTOINCREMENT,
        key BLOB NOT NULL,
        exp INTEGER NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def log_auth(ip, user_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO auth_logs (request_ip, user_id) VALUES (?, ?)",
        (ip, user_id)
    )

    conn.commit()
    conn.close()


def get_keys():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM keys")
    rows = cur.fetchall()

    conn.close()
    return rows