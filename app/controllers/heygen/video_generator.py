import requests
import os

HEYGEN_API_KEY = os.getenv("HEYGEN_API_KEY")

def generate_heygen_video(
    prompt: str,
    api_key: str = HEYGEN_API_KEY,
    avatar_id: str = "Abigail_expressive_2024112501",
    template_id: str = None,
    voice_id: str = "26b2064088674c80b1e5fc5ab1a068ec"
):
    print("arguements ", prompt, api_key, avatar_id, template_id, voice_id)
    
    # Apply defaults if None values are passed
    if api_key is None:
        api_key = HEYGEN_API_KEY
    if avatar_id is None:
        avatar_id = "Abigail_expressive_2024112501"
    if voice_id is None:
        voice_id = "26b2064088674c80b1e5fc5ab1a068ec"
        
    url = "https://api.heygen.com/v2/video/generate"
    
    # Base payload structure
    payload = {
        "dimension": {
            "width": 1280,
            "height": 720
        }
    }
    
    # If template ID is provided, use template-based generation
    if template_id:
        payload["template_id"] = template_id
        payload["template_data"] = {
            "script": prompt
        }
    else:
        # Otherwise use the avatar-based generation
        payload["video_inputs"] = [
            {
                "character": {
                    "type": "avatar",
                    "avatar_id": avatar_id,
                    "avatar_style": "normal"
                },
                "voice": {
                    "type": "text",
                    "input_text": prompt,
                    "voice_id": voice_id
                }
                # "background": {
                #     "type": "color",
                #     "value": "#008000"
                # }
            }
        ]

    headers = {
        "X-Api-Key": api_key,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    print("✅ Payload sent:")
    print(payload)
    return response.json(), response.status_code
    print("🔁 Response returned:")
    print(response.json())


def get_heygen_video_status(video_id: str, api_key: str = HEYGEN_API_KEY):
    # Apply default if None is passed
    if api_key is None:
        api_key = HEYGEN_API_KEY
        
    url = f"https://api.heygen.com/v1/video_status.get?video_id={video_id}"
    headers = {
        "X-Api-Key": api_key
    }

    response = requests.get(url, headers=headers)
    return response.json(), response.status_code
