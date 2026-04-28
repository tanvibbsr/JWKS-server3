import database
import crypto_utils
import time

def insert_key():
    conn = database.get_db()
    cur = conn.cursor()

    # Example private key (you can replace this)
    private_key = "my-secret-private-key"

    # Encrypt the key using AES
    _, encrypted = crypto_utils.encrypt_private_key(private_key)

    # Expiration time (1 hour from now)
    expiration_time = int(time.time()) + 3600

    # Insert into DB (matches your schema exactly)
    cur.execute("""
        INSERT INTO keys (key, exp)
        VALUES (?, ?)
    """, (encrypted, expiration_time))

    conn.commit()
    conn.close()

    print("✅ Key inserted successfully!")

if __name__ == "__main__":
    insert_key()