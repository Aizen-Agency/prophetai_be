from flask import Blueprint, jsonify
from ...models.insights import Insights
from ...extensions import db
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/insights/<int:user_id>', methods=['GET'])
def get_user_insights(user_id):
    try:
        insights = Insights.query.filter_by(user_id=user_id).first()
        
        if not insights:
            return jsonify({
                'message': 'No insights found for this user',
                'data': {
                    'months': {
                        'january': {'articles': 0, 'scripts': 0, 'videos_generated': 0, 'videos_posted': 0},
                        'february': {'articles': 0, 'scripts': 0, 'videos_generated': 0, 'videos_posted': 0},
                        'march': {'articles': 0, 'scripts': 0, 'videos_generated': 0, 'videos_posted': 0},
                        'april': {'articles': 0, 'scripts': 0, 'videos_generated': 0, 'videos_posted': 0},
                        'may': {'articles': 0, 'scripts': 0, 'videos_generated': 0, 'videos_posted': 0},
                        'june': {'articles': 0, 'scripts': 0, 'videos_generated': 0, 'videos_posted': 0},
                        'july': {'articles': 0, 'scripts': 0, 'videos_generated': 0, 'videos_posted': 0},
                        'august': {'articles': 0, 'scripts': 0, 'videos_generated': 0, 'videos_posted': 0},
                        'september': {'articles': 0, 'scripts': 0, 'videos_generated': 0, 'videos_posted': 0},
                        'october': {'articles': 0, 'scripts': 0, 'videos_generated': 0, 'videos_posted': 0},
                        'november': {'articles': 0, 'scripts': 0, 'videos_generated': 0, 'videos_posted': 0},
                        'december': {'articles': 0, 'scripts': 0, 'videos_generated': 0, 'videos_posted': 0}
                    }
                }
            }), 200

        # Get data for all months
        months_data = {
            'january': insights.get_monthly_data('january'),
            'february': insights.get_monthly_data('february'),
            'march': insights.get_monthly_data('march'),
            'april': insights.get_monthly_data('april'),
            'may': insights.get_monthly_data('may'),
            'june': insights.get_monthly_data('june'),
            'july': insights.get_monthly_data('july'),
            'august': insights.get_monthly_data('august'),
            'september': insights.get_monthly_data('september'),
            'october': insights.get_monthly_data('october'),
            'november': insights.get_monthly_data('november'),
            'december': insights.get_monthly_data('december')
        }

        return jsonify({
            'message': 'Insights retrieved successfully',
            'data': {
                'months': months_data
            }
        }), 200

    except Exception as e:
        return jsonify({
            'message': 'Error retrieving insights',
            'error': str(e)
        }), 500

@dashboard_bp.route('/insights/<int:user_id>/update', methods=['POST'])
def update_user_insights(user_id):
    try:
        data = request.get_json()
        insights = Insights.query.filter_by(user_id=user_id).first()
        
        if not insights:
            insights = Insights(user_id=user_id)
            db.session.add(insights)
        
        # Update data for the specified month
        month = data.get('month', datetime.now().strftime('%B').lower())
        insights.update_monthly_data(month, {
            'articles': data.get('articles', 0),
            'scripts': data.get('scripts', 0),
            'videos_generated': data.get('videos_generated', 0),
            'videos_posted': data.get('videos_posted', 0)
        })
        
        db.session.commit()
        
        return jsonify({
            'message': 'Insights updated successfully',
            'data': insights.get_monthly_data(month)
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Error updating insights',
            'error': str(e)
        }), 500 