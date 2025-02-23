import sqlite3
import random
import string
from app.database import get_db_connection

def is_valid_url(url):
    from urllib.parse import urlparse
    parsed = urlparse(url)
    return bool(parsed.scheme and parsed.netloc)

def generate_short_code():
    return "".join(random.choices(string.ascii_letters + string.digits, k=6))

def insert_url(original_url, short_code):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO urls (short_code, original_url) VALUES (?, ?)", (short_code, original_url))
        conn.commit()

def get_original_url(short_code):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT original_url FROM urls WHERE short_code = ? AND created_at > datetime('now', '-30 days')", (short_code,))
        return cursor.fetchone()

def get_all_urls():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT short_code, original_url, created_at FROM urls")
        return cursor.fetchall()
