from flask import Flask, request, jsonify
import database
import auth_utils
import crypto_utils
import time


app = Flask(__name__)

database.init_db()


# ---------------- REGISTER ----------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data["username"]
    email = data["email"]

    password = auth_utils.create_user(username, email)

    return jsonify({"password": password}), 201


# ---------------- AUTH ----------------
@app.route("/auth", methods=["POST"])
def auth():
    ip = request.remote_addr

    
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    user = auth_utils.verify_user(username, password)

    if not user:
        database.log_auth(ip, None)
        return jsonify({"error": "invalid credentials"}), 401

    database.log_auth(ip, user["id"])
    return jsonify({"status": "success"}), 200


# ---------------- JWKS ----------------
@app.route("/jwks", methods=["GET"])
def jwks():
    conn = database.get_db()
    cur = conn.cursor()

    # Only get non-expired keys
    cur.execute("SELECT * FROM keys WHERE exp > ?", (int(time.time()),))
    keys = cur.fetchall()

    jwks_keys = []

    for key in keys:
        decrypted = crypto_utils.decrypt_private_key(None, key["key"])

        jwks_keys.append({
            "kid": str(key["kid"]),
            "key": decrypted
        })

    conn.close()

    return jsonify({"keys": jwks_keys}), 200

if __name__ == "__main__":
    app.run(debug=True)