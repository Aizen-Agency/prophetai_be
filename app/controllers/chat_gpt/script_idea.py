import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_script_ideas(product_name, description, script_idea, twitter_content=None):
    try:
        # Construct the prompt
        prompt = f"""Generate 50 unique and engaging script ideas for a product called '{product_name}'.
        
Product Description: {description}

User's Script Idea Requirements: {script_idea}


Generate 50 different script ideas that:
1. Are creative and engaging
2. Incorporate the product's key features
3. Follow the user's requirements
4. Are suitable for social media content
5. Include a clear call-to-action

Format each idea as a JSON object with:
- title: A catchy title
- content: The full script content
- focus: Key themes/topics covered

Return a JSON object with a 'scriptIdeas' key containing an array of ideas. Example format:
{{
    "scriptIdeas": [
        {{
            "title": "Example Title",
            "content": "Example content",
            "focus": "Example focus"
        }}
    ]
}}"""

        # Call ChatGPT API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a creative content strategist specializing in social media marketing. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000,
            response_format={ "type": "json_object" }
        )

        # Get the response content
        response_content = response.choices[0].message.content
        
        # Try to parse the response
        try:
            # Parse the JSON response
            response_data = json.loads(response_content)
            
            # Extract ideas from either format
            if isinstance(response_data, dict) and 'scriptIdeas' in response_data:
                ideas = response_data['scriptIdeas']
            elif isinstance(response_data, list):
                ideas = response_data
            else:
                raise ValueError("Invalid response format")
                
            # Validate the structure
            if not isinstance(ideas, list):
                raise ValueError("Response is not a list of ideas")
                
            for idea in ideas:
                if not all(key in idea for key in ['title', 'content', 'focus']):
                    raise ValueError("Missing required fields in idea object")
            
            return {
                "message": "Script ideas generated successfully",
                "ideas": ideas
            }
            
        except json.JSONDecodeError as e:
            print(f"[ERROR] Failed to parse JSON response: {str(e)}")
            print(f"[DEBUG] Response content: {response_content}")
            return {
                "error": "Failed to parse script ideas",
                "details": str(e)
            }
        except ValueError as e:
            print(f"[ERROR] Invalid response structure: {str(e)}")
            print(f"[DEBUG] Response content: {response_content}")
            return {
                "error": "Invalid response structure",
                "details": str(e)
            }

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return {
            "error": "Failed to generate script ideas",
            "details": str(e)
        }