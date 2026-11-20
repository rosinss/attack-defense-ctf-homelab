from flask import Flask, request, jsonify
import logging
import os
import secrets

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

USERS = {
    "alice": {"role": "user", "balance": 100},
    "bob": {"role": "user", "balance": 200},
    "admin": {"role": "admin", "balance": 999}
}

# Tokens come from environment variables, not client usernames.
TOKENS = {
    os.environ["ALICE_TOKEN"]: "alice",
    os.environ["BOB_TOKEN"]: "bob",
    os.environ["ADMIN_TOKEN"]: "admin"
}


@app.route("/")
def home():
    return jsonify({
        "service": "I-HACK Defender Lab",
        "status": "running"
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/profile")
def profile():
    username = request.args.get("user")
    authorization = request.headers.get("Authorization", "")

    if not authorization.startswith("Bearer "):
        return jsonify({"error": "Authentication required"}), 401

    token = authorization[7:]
    authenticated_user = None

    for known_token, owner in TOKENS.items():
        if secrets.compare_digest(token, known_token):
            authenticated_user = owner
            break

    if authenticated_user is None:
        app.logger.warning("Rejected invalid authentication token")
        return jsonify({"error": "Invalid token"}), 401

    if username not in USERS:
        return jsonify({"error": "User not found"}), 404

    if authenticated_user != username:
        app.logger.warning(
            "Denied profile access: %s attempted %s",
            authenticated_user,
            username
        )
        return jsonify({"error": "Access denied"}), 403

    return jsonify({
        "username": username,
        "data": USERS[username]
    })

@app.route("/challenge/flag")
def challenge_flag():
    flag = "ihack{practice_flag_123}"

    if request.args.get("key") == "training":
        return jsonify({"flag": flag})

    return jsonify({"error": "Access denied"}), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

