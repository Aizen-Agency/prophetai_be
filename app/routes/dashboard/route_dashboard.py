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

        # Get count of scripts for the user
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM scripts WHERE user_id = %s", (user_id,))
        scripts_count = cur.fetchone()['count']
        
        # Get count of videos for the user
        cur.execute("SELECT COUNT(*) FROM videos WHERE user_id = %s", (user_id,))
        videos_count = cur.fetchone()['count']
        
        cur.close()
        conn.close()

        return jsonify({
            'message': 'User data retrieved successfully',
            'data': {
                'total_articles_scraped': insights.articles_scraped,
                'total_videos_posted': insights.videos_posted,
                'total_scripts_generated': scripts_count,
                'total_videos_created': videos_count,
                'account_created_at': insights.created_at.isoformat()
            }
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