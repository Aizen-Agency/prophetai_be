from flask import Blueprint, jsonify, request
from ...models.userData import User
from app.extensions import get_db_connection
from datetime import datetime
from app.models.insights import Insights
from app.models.scriptsModel import Script
from app.models.videoModel import Video

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/insights/<int:user_id>', methods=['GET'])
def get_user_insights(user_id):
    try:
        # Get user's insights
        insights = Insights.get_by_user(user_id)
        
        if not insights:
            insights = Insights(user_id=user_id)
            insights.save()

        # Prepare monthly data
        monthly_data = []
        for month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']:
            monthly_data.append({
                'name': month.capitalize(),
                'articles': getattr(insights, f'{month}_total_articles_scraped'),
                'scripts': getattr(insights, f'{month}_total_scripts_generated'),
                'totalVideos': getattr(insights, f'{month}_total_videos_generated')
            })

        return jsonify({
            'message': 'User data retrieved successfully',
            'data': monthly_data
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/insights/<int:user_id>/update', methods=['POST'])
def update_user_insights(user_id):
    try:
        data = request.get_json()
        videos_posted = data.get('videos_posted', 0)

        # Get or create insights for user
        insights = Insights.get_by_user(user_id)
        if not insights:
            insights = Insights(user_id=user_id)
            insights.save()

        # Update videos posted count
        insights.videos_posted = videos_posted
        insights.update()

        return jsonify({
            'message': 'Insights updated successfully',
            'data': {
                'videos_posted': videos_posted
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500 