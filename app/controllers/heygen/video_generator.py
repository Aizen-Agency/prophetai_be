import requests
import os

HEYGEN_API_KEY = os.getenv("HEYGEN_API_KEY")

def generate_heygen_video(prompt: str):
    url = "https://api.heygen.com/v2/video/generate"
    
    payload = {
        "video_inputs": [
            {
                "character": {
                    "type": "avatar",
                    "avatar_id": "Daisy-inskirt-20220818",
                    "avatar_style": "normal"
                },
                "voice": {
                    "type": "text",
                    "input_text": prompt,
                    "voice_id": "2d5b0e6cf36f460aa7fc47e3eee4ba54"
                },
                "background": {
                    "type": "color",
                    "value": "#008000"
                }
            }
        ],
        "dimension": {
            "width": 1280,
            "height": 720
        }
    }

    headers = {
        "X-Api-Key": HEYGEN_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json(), response.status_code


def get_heygen_video_status(video_id: str):
    url = f"https://api.heygen.com/v1/video_status.get?video_id={video_id}"
    headers = {
        "X-Api-Key": HEYGEN_API_KEY
    }

    response = requests.get(url, headers=headers)
    return response.json(), response.status_code
