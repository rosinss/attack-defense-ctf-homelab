from flask import Flask, request, jsonify
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB_PATH = Path(__file__).resolve().parent / "employees.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT,
                department TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS secrets (
                id INTEGER PRIMARY KEY,
                flag TEXT
            )
        """)
        conn.execute("DELETE FROM employees")
        conn.execute("DELETE FROM secrets")
        conn.executemany(
            "INSERT INTO employees VALUES (?, ?, ?)",
            [
                (1, "Alice", "IT"),
                (2, "Bob", "Finance"),
                (3, "Charlie", "HR")
            ]
        )
        conn.execute(
            "INSERT INTO secrets VALUES (?, ?)",
            (1, "ihack{sqli_practice_success}")
        )

@app.route("/")
def home():
    return jsonify({
        "service": "Employee Portal",
        "endpoints": ["/health", "/employees?name=Alice"]
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/employees")
def employees():
    name = request.args.get("name", "")

    with get_db() as conn:
    	query = "SELECT id, name, department FROM employees WHERE name = ?"
    	rows = conn.execute(query, (name,)).fetchall()

    return jsonify([dict(row) for row in rows])

if __name__ == "__main__":
    initialize_db()
    app.run(host="127.0.0.1", port=5004)
