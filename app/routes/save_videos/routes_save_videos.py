from flask import Blueprint, request, jsonify
from ...models.videoModel import Video
from ...models.scriptsModel import Script
import uuid
import os
from datetime import datetime

video_bp = Blueprint('video', __name__)

# Dummy S3 functionality
def upload_to_s3( filename):
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
        user_id = data.get('user_id')
        script_id = data.get('script_id')


        if not all([user_id, script_id]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Generate unique filename
        filename = f"{uuid.uuid4()}.mp4"
        
        # Upload to S3 (dummy implementation)
        video_url = upload_to_s3( filename)
        
        # Create video record
        video = Video(
            user_id=user_id,
            script_id=script_id,
            video_url=video_url,
            size="50MB",  # Dummy size
            created_at=datetime.now()
        )
        video.save()

        return jsonify({
            'message': 'Video generated and saved successfully',
            'video': {
                'id': video.id,
                'url': video.video_url,
                'created_at': video.created_at
            }
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@video_bp.route('/videos/<int:user_id>', methods=['GET'])
def get_user_videos(user_id):
    try:
        # Get all videos for the user
        videos = Video.get_by_user(user_id)
        
        return jsonify({
            'videos': [{
                'id': video.id,
                'url': video.video_url,
                'created_at': video.created_at,
                'size': video.size
            } for video in videos]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500 