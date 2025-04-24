from flask import Blueprint, request, jsonify
from app.controllers.apify.instagram_scraper import scrape_instagram_profile_posts
from app.controllers.chat_gpt.calculate_analytics import calculate_instagram_analytics
from app.extensions import get_db_connection
from app.models.analytics import Analytics

api_instagram = Blueprint("instagram", __name__, url_prefix="")

@api_instagram.route('/instagram-analytics', methods=['GET'])
def get_instagram_analytics():
    try:
        # Fetch analytics data from the database
        analytics_data = Analytics.get_all()
        analytics_list = [analytics.to_dict() for analytics in analytics_data]

        return jsonify({
            "message": "Analytics data retrieved successfully",
            "analytics": analytics_list
        }), 200

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

# @api_instagram.route('/instagram-analytics', methods=['POST'])
# def instagram_analytics():
#     try:
#         data = request.get_json()
        
#         # Validate request data
#         if not data:
#             return jsonify({"error": "No data provided"}), 400
            
#         # Extract and validate required fields
#         profile_url = data.get('profile_url')
#         if not profile_url:
#             return jsonify({"error": "Missing required field: profile_url"}), 400

#         # First scrape the Instagram profile
#         scraped_data, status_code = scrape_instagram_profile_posts(profile_url)
        
#         if status_code != 200:
#             return jsonify(scraped_data), status_code

#         # Then calculate analytics from the scraped data
#         analytics = calculate_instagram_analytics(scraped_data.get('posts', []))
        
#         return jsonify(analytics), 200

#     except Exception as e:
#         print(f"[ERROR] {str(e)}")
#         return jsonify({"error": "An unexpected error occurred"}), 500
