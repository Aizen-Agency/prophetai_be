from flask import Blueprint, jsonify, request
from app.models.videoModel import Video
from app.models.userData import User
from app.extensions import get_db_connection

admin_bp = Blueprint('admin_routes', __name__)

@admin_bp.route('/admin/videos', methods=['GET'])
def get_all_videos():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get all videos with user information using a JOIN query
        cur.execute("""
            SELECT v.*, u.firstname, u.lastname, u.email
            FROM videos v
            JOIN userData u ON v.user_id = u.id
        """)
        
        videos = cur.fetchall()
        cur.close()
        conn.close()
        
        # Format the response
        video_list = []
        for video in videos:
            video_list.append({
                'id': video['id'],
                'user': {
                    'id': video['user_id'],
                    'name': f"{video['firstname']} {video['lastname']}",
                    'email': video['email']
                },
                'video_url': video['video_url'],
                'size': video['size'],
                'created_at': video['created_at']
            })
        
        return jsonify({
            'message': 'Videos retrieved successfully',
            'videos': video_list
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/users', methods=['GET'])
def get_all_users():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get all users
        cur.execute("""
            SELECT id, firstname, lastname, email, created_at
            FROM userData
        """)
        
        users = cur.fetchall()
        cur.close()
        conn.close()
        
        # Format the response
        user_list = []
        for user in users:
            user_list.append({
                'id': user['id'],
                'name': f"{user['firstname']} {user['lastname']}",
                'email': user['email'],
                'created_at': user['created_at']
            })
        
        return jsonify({
            'message': 'Users retrieved successfully',
            'users': user_list
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
