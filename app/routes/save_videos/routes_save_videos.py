from flask import Blueprint, request, jsonify
from ...models.videoModel import Video
from ...models.scriptsModel import Script
from ...models.insights import Insights
from ...controllers.S3.awsS3 import s3_service
from ...controllers.heygen.video_generator import generate_heygen_video, get_heygen_video_status
from ...extensions import get_db_connection
import uuid
import os
from datetime import datetime
import requests
import time
from io import BytesIO

video_bp = Blueprint('video', __name__)
HEYGEN_API_KEY = os.getenv("HEYGEN_API_KEY")


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
        transcript = data.get('transcript')
        heygen_settings = data.get('heygen', {})

        if not all([user_id, script_id, transcript]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Get script content from database
        script = Script.get_by_id_and_user(script_id, user_id)
        if not script:
            return jsonify({'error': 'Script not found'}), 404

        # Set up HeyGen configuration
        api_key = None
        avatar_id = None
        template_id = None
        voice_id = None
        
        # Use custom settings if provided and not using defaults
        if heygen_settings and not heygen_settings.get('useDefault', False):
            api_key = heygen_settings.get('apiKey')
            avatar_id = heygen_settings.get('avatarId')
            template_id = heygen_settings.get('templateId')
            voice_id = heygen_settings.get('voiceId')

        # Generate video using HeyGen with the script content
        heygen_response, status_code = generate_heygen_video(
            script.script_content,
            api_key=api_key,
            avatar_id=avatar_id,
            template_id=template_id,
            voice_id=voice_id
        )
        
        if status_code != 200:
            return jsonify({'error': 'Failed to generate video with HeyGen'}), status_code

        video_id = heygen_response.get('data', {}).get('video_id')
        if not video_id:
            return jsonify({'error': 'No video ID received from HeyGen'}), 500

        # Poll for video completion (just to ensure it's processing)
        max_attempts = 5  # just to give quick feedback
        attempts = 0
        video_status = None

        while attempts < max_attempts:
            status_data, status_code = get_heygen_video_status(video_id, api_key)
            if status_code == 200:
                video_status = status_data.get('data', {}).get('status')
                if video_status == 'completed':
                    video_url = status_data['data']['video_url']
                    break
                elif video_status == 'failed':
                    return jsonify({'error': 'HeyGen video generation failed'}), 500
            time.sleep(3)
            attempts += 1

        return jsonify({
            'message': 'HeyGen video generation initiated',
            'video_id': video_id,
            'status': video_status,
            'note': 'Once the video is ready, call /upload-heygen-video with the video_id to store it in S3 and get a download link.'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@video_bp.route('/upload-heygen-video', methods=['POST'])
def upload_heygen_video():
    data = request.get_json()
    video_id = data.get('video_id')
    user_id = data.get('user_id')
    script_id = data.get('script_id')

    if not all([video_id, user_id, script_id]):
        return jsonify({"error": "video_id, user_id, and script_id are required"}), 400

    try:
        # Fetch the original script ID using the idea_id
        script = Script.get_by_user_and_idea_id(user_id, script_id)
        if not script:
            return jsonify({"error": "Script not found"}), 404

        # Use the original script ID
        original_script_id = script.id

        # Check if video already exists for this script
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM videos WHERE user_id = %s AND script_id = %s", (user_id, original_script_id))
        existing_video = cur.fetchone()
        cur.close()
        conn.close()

        if existing_video:
            return jsonify({
                "message": "Video for this script already exists",
                "video_id": existing_video['id'],
                "presigned_url": existing_video['video_url'],
                "status": "completed"
            }), 200

        # Check HeyGen video status
        headers = {"X-Api-Key": HEYGEN_API_KEY}
        video_status_url = f"https://api.heygen.com/v1/video_status.get?video_id={video_id}"
        
        print("⏳ Checking video status...")
        response = requests.get(video_status_url, headers=headers)
        response.raise_for_status()
        status_data = response.json()["data"]
        status = status_data["status"]
        
        # Return current status if not completed
        if status != "completed":
            return jsonify({
                "status": status,
                "message": f"Video is currently {status}. Please check back later."
            }), 202  # 202 Accepted means the request was valid but processing is not complete
        
        # If video is completed, process it
        video_url = status_data["video_url"]
        thumbnail_url = status_data.get("thumbnail_url", "")
        print(f"✅ Video completed! Downloading from: {video_url}")

        # Download video in memory
        video_response = requests.get(video_url, stream=True)
        video_response.raise_for_status()

        buffer = BytesIO(video_response.content)

        # Define S3 key
        s3_key = f"videos/heygen_{video_id}.mp4"

        # Upload to S3
        s3_service.s3_client.upload_fileobj(buffer, s3_service.bucket_name, s3_key)
        print("🎉 Upload to S3 successful!")

        # Get presigned URL
        presigned_url = s3_service.get_presigned_url(s3_key)

        # Save video details to the database
        video = Video(user_id=user_id, script_id=original_script_id, video_url=presigned_url, size='unknown')
        video.save()
        
        # Update insights for the current month
        current_month = datetime.now().strftime('%b').lower()  # Get current month abbreviation in lowercase
        insights = Insights.get_by_user(user_id)
        
        if insights:
            # Increment video count for the current month
            insights.update_monthly_data(current_month, articles=0, scripts=0, videos=1)
            print(f"✅ Updated insights for user {user_id} - incremented {current_month}_total_videos_generated")
        else:
            # Create new insights record if it doesn't exist
            new_insights = Insights(user_id=user_id)
            new_insights.save()
            new_insights.update_monthly_data(current_month, articles=0, scripts=0, videos=1)
            print(f"✅ Created new insights for user {user_id} with {current_month}_total_videos_generated = 1")

        return jsonify({
            "message": "Video uploaded to S3 successfully",
            "s3_key": s3_key,
            "presigned_url": presigned_url,
            "thumbnail_url": thumbnail_url,
            "status": "completed"
        }), 200

    except Exception as e:
        print(f"❌ Exception occurred: {e}")
        return jsonify({"error": str(e), "status": "failed"}), 500

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
