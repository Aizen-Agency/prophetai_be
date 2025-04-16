from flask import Blueprint, jsonify, request
from ...models.insights import Insights
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/insights/<int:user_id>', methods=['GET'])
def get_user_insights(user_id):
    try:
        insights = Insights.get_by_user(user_id)
        
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

        # Get current month
        current_month = datetime.now().strftime('%B').lower()
        
        # Get data for all months
        months_data = {}
        months = ['january', 'february', 'march', 'april', 'may', 'june', 
                 'july', 'august', 'september', 'october', 'november', 'december']
        
        for month in months:
            months_data[month] = insights.get_monthly_data(month)

        return jsonify({
            'message': 'Insights retrieved successfully',
            'data': {
                'months': months_data,
                'current_month': current_month
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/insights/<int:user_id>/update', methods=['POST'])
def update_user_insights(user_id):
    try:
        data = request.get_json()
        month = data.get('month')
        metrics = data.get('metrics')

        if not month or not metrics:
            return jsonify({'error': 'Missing month or metrics data'}), 400

        # Get or create insights for user
        insights = Insights.get_by_user(user_id)
        if not insights:
            insights = Insights(user_id=user_id)
            insights.save()

        # Update metrics for the specified month
        insights.update_monthly_data(month, metrics)

        return jsonify({
            'message': 'Insights updated successfully',
            'data': {
                'month': month,
                'metrics': metrics
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500 