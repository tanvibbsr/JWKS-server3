import uuid
from argon2 import PasswordHasher
import database

ph = PasswordHasher()


def create_user(username, email):
    password = str(uuid.uuid4())
    password_hash = ph.hash(password)

    conn = database.get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
        (username, password_hash, email)
    )

    conn.commit()
    conn.close()

    return password


def verify_user(username, password):
    conn = database.get_db()
    cur = conn.cursor()

    cur.execute("SELECT id, password_hash FROM users WHERE username=?", (username,))
    user = cur.fetchone()

    conn.close()

    if not user:
        return None

    try:
        ph.verify(user["password_hash"], password)
        return {"id": user["id"]}
    except:
        return None