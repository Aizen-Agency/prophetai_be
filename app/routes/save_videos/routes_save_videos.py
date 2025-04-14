from flask import Blueprint, request, jsonify
from ...models.videoModel import Video
from ...models.scriptsModel import Script
from ...extensions import db
import uuid
import os
from datetime import datetime

video_bp = Blueprint('video', __name__)

# Dummy S3 functionality
def upload_to_s3(video_data, filename):
    """
    Dummy function to simulate S3 upload
    Returns a dummy S3 URL
    """
    # In a real implementation, this would upload to actual S3
    # For now, we'll return a dummy URL
    return f"https://dummy-s3-bucket.s3.amazonaws.com/videos/{filename}"

@video_bp.route('/generate-video', methods=['POST'])
def generate_video():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['user_id', 'script_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if script exists
        script = Script.query.get(data['script_id'])
        # if not script:
        #     return jsonify({'error': f'Script with id {data["script_id"]} not found'}), 404
        
        # Generate a unique filename
        filename = f"{uuid.uuid4()}.mp4"
        
        # Simulate video generation and S3 upload
        video_url = upload_to_s3(None, filename)
        
        # Create new video record
        new_video = Video(
            user_id=data['user_id'],
            script_id=data['script_id'],
            video_url=video_url,
            size="50MB"  # Dummy size
        )
        
        db.session.add(new_video)
        db.session.commit()
        
        return jsonify({
            'message': 'Video generated successfully',
            'video_id': new_video.id,
            'video_url': video_url
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@video_bp.route('/videos/<int:user_id>', methods=['GET'])
def get_user_videos(user_id):
    try:
        videos = Video.query.filter_by(user_id=user_id).all()
        return jsonify([{
            'id': video.id,
            'script_id': video.script_id,
            'video_url': video.video_url,
            'size': video.size,
            'created_at': video.created_at.isoformat()
        } for video in videos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 