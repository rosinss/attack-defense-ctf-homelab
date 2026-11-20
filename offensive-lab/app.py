from flask import Flask, request, jsonify

app = Flask(__name__)

USERS = {
    "alice": {
        "role": "user",
        "balance": 100
    },
    "bob": {
        "role": "user",
        "balance": 200
    },
    "admin": {
        "role": "admin",
        "balance": 999,
        "flag": "ihack{idor_practice_success}"
    }
}

TOKENS = {
    "alice-token": "alice",
    "bob-token": "bob"
}

@app.route("/")
def home():
    return jsonify({
        "service": "A&D Offensive Practice",
        "status": "running"
    })

@app.route("/profile")
def profile():
    token = request.headers.get("Authorization", "").removeprefix("Bearer ")
    authenticated_user = TOKENS.get(token)

    if not authenticated_user:
        return jsonify({"error": "Authentication required"}), 401

    username = request.args.get("user", authenticated_user)

    if username not in USERS:
        return jsonify({"error": "User not found"}), 404
	
    if authenticated_user != username:
    return jsonify({"error": "Access denied"}), 403    

    # Intentionally vulnerable: missing authorization check
    return jsonify({
        "username": username,
        "data": USERS[username]
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
