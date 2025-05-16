import openai
from dotenv import load_dotenv
import os
from ...controllers.prompts.video_prompts import get_video_prompts

load_dotenv()

client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_scripts_with_chatgpt(product_name=None, description=None, script_idea=None, twitter_content=None):
    """
    Generate different types of video scripts using ChatGPT with different prompts
    """
    # Get the video prompts
    prompts = get_video_prompts(product_name, description, script_idea, twitter_content)
    
    scripts = []
    
    for i, prompt in enumerate(prompts):
        try:
            # Prepare the prompt with available variables
            formatted_prompt = prompt
            if product_name:
                formatted_prompt = formatted_prompt.replace("INSERT TRANSCRIPT", product_name)
            if description:
                formatted_prompt = formatted_prompt.replace("INSERT FOUNDER TRANSCRIPT", description)
            if script_idea:
                formatted_prompt = formatted_prompt.replace("INSERT ORIGINAL POST COPY", script_idea)
            if twitter_content:
                formatted_prompt = formatted_prompt.replace("[INSERT TRENDING VIDEO TRANSCRIPT HERE]", twitter_content)
                formatted_prompt = formatted_prompt.replace("**[INSERT TRENDING VIDEO TRANSCRIPT HERE]**", twitter_content)

            script_type = [
                "Talking Head Video",
                "Fake Podcast",
                "Reaction Video (Mid Roll)",
                "Reaction Video (End Roll)",
                "Video Titles"
            ][i]

            # Print the formatted prompt before sending to ChatGPT
            print(f"\nSending prompt to ChatGPT for {script_type}:")
            print("----------------------------------------")
            print(formatted_prompt)
            print("----------------------------------------\n")

            system_message = "You are a professional video content creator specializing in short-form video content. Provide ONLY the final script text without any template formatting or explanations."
            
            # For reaction videos, we need special handling for [SHOW CLIP] markers
            if "Reaction Video" in script_type:
                system_message = "You are a professional video content creator specializing in short-form video content. Provide the final script text INCLUDING the [SHOW CLIP] marker where appropriate. Do not include any other formatting, section markers, or explanations."

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": formatted_prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            script_content = response.choices[0].message.content
            
            scripts.append({
                'id': f'copy{i+1}',
                'title': f"({script_type})",
                'content': script_content,
                'type': script_type.lower().replace(' ', '_')
            })
            
        except Exception as e:
            print(f"Error generating script {i+1}: {str(e)}")
            continue
    
    return scripts
