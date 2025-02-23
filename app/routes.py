from flask import Blueprint, request, jsonify, redirect, current_app
from app.models import insert_url, get_original_url, get_all_urls, is_valid_url, generate_short_code

routes = Blueprint("routes", __name__)

# Basic route
@routes.route("/")
def home():
    return "Home"

# Route to shorten the the given URL(POST)
@routes.route("/shorten", methods=["POST"])
def shorten():
    data = request.get_json()
    original_url = data.get("url")

    if not original_url or not is_valid_url(original_url):
        return jsonify({"error": "Invalid URL"}), 400
    
    short_code = generate_short_code()
    insert_url(original_url, short_code)

    short_url = request.host_url + short_code
    return jsonify({"short_url": short_url})

# Route to get the original URL from the shortened one(GET)
@routes.route("/<short_code>", methods=["GET"])
def redirect_to_original(short_code):
    result = get_original_url(short_code)

    if result:
        return redirect(result[0])
    else:
        return jsonify({"error": "URL not found or expired"}), 404

# Route to get all the URLs(GET)
@routes.route("/urls", methods=["GET"])
def list_all_urls():
    urls = get_all_urls()
    return jsonify([
        {"short_url": request.host_url + row[0], "original_url": row[1], "created_at": row[2]}
        for row in urls
    ])
