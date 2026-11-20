from flask import Flask, request, jsonify, send_file
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR / "public"

@app.route("/")
def home():
    return jsonify({
        "service": "I-HACK File Server",
        "status": "running",
        "download": "/download?file=welcome.txt"
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/download")
def download():
    filename = request.args.get("file", "")

    if not filename:
        return jsonify({"error": "Missing filename"}), 400

    # Intentionally vulnerable for local CTF training.
    target = (PUBLIC_DIR / filename).resolve()

    if not target.is_relative_to(PUBLIC_DIR.resolve()):
    	return jsonify({"error": "Access denied"}), 403

    if not target.is_file():
    	return jsonify({"error": "File not found"}), 404

    return send_file(target)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5003)
