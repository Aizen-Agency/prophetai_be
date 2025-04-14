from flask import Blueprint, jsonify, request
from app.models.videoModel import Video
from app.models.userData import User
from app import db

admin_bp = Blueprint('admin_routes', __name__)

@admin_bp.route('/admin/videos', methods=['GET'])
def get_all_videos():
    try:
        # Get all videos with user information
        videos = db.session.query(Video, User).join(User, Video.user_id == User.id).all()
        
        # Format the response
        video_list = []
        for video, user in videos:
            video_list.append({
                'id': video.id,
                'name': video.name,
                'size': video.size,
                'thumbnail': video.thumbnail,
                'userId': video.user_id,
                'aiModel': video.ai_model,
                'duration': video.duration,
                'quality': video.quality,
                'createdAt': video.created_at.strftime('%Y-%m-%d'),
                'user': {
                    'id': user.id,
                    'name': f"{user.firstname} {user.lastname}",
                    'email': user.email,
                    'avatar': user.avatar
                }
            })
        
        return jsonify({
            'success': True,
            'videos': video_list
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
