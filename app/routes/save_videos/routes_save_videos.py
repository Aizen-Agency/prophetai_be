from flask import Blueprint, request, jsonify
from ...models.videoModel import Video
from ...models.scriptsModel import Script
from ...controllers.S3.awsS3 import s3_service
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
        video_file = request.files.get('video')

        if not all([user_id, script_id, video_file]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Generate unique filename
        filename = f"{uuid.uuid4()}.mp4"
        
        # Save the file temporarily
        temp_path = f"/tmp/{filename}"
        video_file.save(temp_path)
        
        # Upload to S3
        if not s3_service.upload_file(temp_path, filename):
            return jsonify({'error': 'Failed to upload video to S3'}), 500
            
        # Get the S3 URL
        video_url = s3_service.get_object_url(filename)
        
        # Clean up temporary file
        os.remove(temp_path)
        
        # Create video record
        video = Video(
            user_id=user_id,
            script_id=script_id,
            video_url=video_url,
            size=os.path.getsize(temp_path),  # Get actual file size
            created_at=datetime.now()
        )
        video.save()

        return jsonify({
            'message': 'Video generated and saved successfully',
            'video': {
                'id': video.id,
                'url': video.video_url,
                'created_at': video.created_at,
                'size': video.size
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