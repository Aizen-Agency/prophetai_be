from flask import Blueprint, request, jsonify
from app.controllers.apify.instagram_scraper import scrape_instagram_posts_controller

api_instagram = Blueprint("instagram", __name__, url_prefix="")

@api_instagram.route('/scrape-instagram', methods=['POST'])
def scrape_instagram():
    try:
        data = request.get_json()
        
        # Validate request data
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        # Extract and validate required fields
        profile_url = data.get('profile_url')
        if not profile_url:
            return jsonify({"error": "Missing required field: profile_url"}), 400

        # Call the scraper controller
        result, status_code = scrape_instagram_posts_controller(profile_url)
        
        return jsonify(result), status_code

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500
