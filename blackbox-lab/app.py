from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "service": "Employee Portal",
        "message": "Welcome to the portal",
        "links": ["/api/help", "/api/me"]
    })

@app.route("/api/help")
def help_page():
    return jsonify({
        "authentication": "Bearer guest-token",
        "profile_endpoint": "/api/me",
        "documents": "/api/documents/<document_id>"
    })

@app.route("/api/me")
def me():
    token = request.headers.get("Authorization", "")
    if token != "Bearer guest-token":
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({
        "username": "guest",
        "role": "employee",
        "documents": [100]
    })

@app.route("/api/documents/<int:document_id>")
def document(document_id):
    token = request.headers.get("Authorization", "")
    if token != "Bearer guest-token":
        return jsonify({"error": "Unauthorized"}), 401

    documents = {
        100: {"title": "Employee Handbook", "content": "Welcome!"},
        101: {"title": "Admin Notes", "flag": "ihack{blackbox_idor_solved}"}
    }

    if document_id not in documents:
        return jsonify({"error": "Not found"}), 404

    if document_id != 100:
        return jsonify({"error": "Access denied"}), 403

    return jsonify(documents[document_id])

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002)
