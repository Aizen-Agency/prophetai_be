from flask import Blueprint, request, jsonify
from ...models.videoModel import Video
from ...models.scriptsModel import Script
from ...controllers.S3.awsS3 import s3_service
from ...controllers.heygen.video_generator import generate_heygen_video, get_heygen_video_status
import uuid
import os
from datetime import datetime
import requests
import time

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
        prompt = data.get('prompt')
        transcript = data.get('transcript')
        script_content = data.get('script_content')

        if not all([user_id, script_id, prompt, transcript, script_content]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Generate video using HeyGen
        heygen_response, status_code = generate_heygen_video(prompt)
        
        if status_code != 200:
            return jsonify({'error': 'Failed to generate video with HeyGen'}), status_code
            
        video_id = heygen_response.get('data', {}).get('video_id')
        if not video_id:
            return jsonify({'error': 'No video ID received from HeyGen'}), 500

        # Poll for video completion
        max_attempts = 30  # 5 minutes with 10-second intervals
        attempts = 0
        video_url = None

        while attempts < max_attempts:
            status_data, status_code = get_heygen_video_status(video_id)
            if status_code == 200 and status_data.get('data', {}).get('status') == 'completed':
                video_url = status_data.get('data', {}).get('video_url')
                break
            time.sleep(10)  # Wait 10 seconds before next attempt
            attempts += 1

        if not video_url:
            return jsonify({'error': 'Video generation timed out'}), 504

        # Download the video from HeyGen
        response = requests.get(video_url)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to download video from HeyGen'}), 500

        # Generate unique filename
        filename = f"{uuid.uuid4()}.mp4"
        temp_path = f"/tmp/{filename}"
        
        # Save the video temporarily
        with open(temp_path, 'wb') as f:
            f.write(response.content)
        
        # Upload to S3
        if not s3_service.upload_file(temp_path, filename):
            return jsonify({'error': 'Failed to upload video to S3'}), 500
            
        # Get the S3 URL
        s3_video_url = s3_service.get_object_url(filename)
        
        # Clean up temporary file
        os.remove(temp_path)
        
        # Create video record
        video = Video(
            user_id=user_id,
            script_id=script_id,
            video_url=s3_video_url,
            size=os.path.getsize(temp_path),
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


# @heygen_api.route("/check-status/<video_id>", methods=["GET"])
# def check_video_status(video_id):
#     status_data, status_code = get_heygen_video_status(video_id)
#     return jsonify(status_data), status_code