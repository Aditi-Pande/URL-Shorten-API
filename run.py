from flask import Flask, request, jsonify, redirect
import sqlite3
import random
import string
import datetime
from urllib.parse import urlparse

app = Flask(__name__)

db = "url.db"


def setup_db():
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_code TEXT UNIQUE NOT NULL,
                original_url TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

@app.route("/")
def home():
    return "Home"

def is_valid_url(url):
    check = urlparse(url)

    if check.netloc and check.scheme:
        return True
    else:
        return False

def generate_short_code():
    return "".join(random.choices(string.ascii_letters + string.digits, k = 6))

@app.route("/shorten", methods=["POST"])
def shorten():
    data = request.get_json()
    original_url = data.get("url")

    if not original_url or not is_valid_url(original_url):
        return jsonify("Invalid URL !!", 400)
    
    short_code = generate_short_code()

    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO urls (short_code, original_url) VALUES (?, ?)", (short_code, original_url))
        conn.commit()

    short_url = request.host_url + short_code
    return jsonify({"short_url": short_url})

@app.route("/<short_code>", methods=["GET"])
def redirect_to_original(short_code):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT original_url FROM urls WHERE short_code = ? AND created_at > datetime('now', '-30 days')", (short_code,))
        result = cursor.fetchone()
    
    if result:
        return redirect(result[0])
    else:
        return jsonify("URL not found or expired"), 404

@app.route("/urls", methods=["GET"])
def list_all_urls():
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT short_code, original_url, created_at FROM urls")
        urls = [
            {
                "short_url": request.host_url + row[0],
                "original_url": row[1],
                "created_at": row[2]
            }
            for row in cursor.fetchall()
        ]
    return jsonify(urls)

if __name__ == "__main__":
    setup_db()
    app.run(host="0.0.0.0", debug=True)
