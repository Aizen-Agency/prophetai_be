import openai
from dotenv import load_dotenv
import os

load_dotenv()

client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_scripts_with_chatgpt(product_name, description, script_idea, twitter_content=None):
    """
    Generate 6 different scripts using ChatGPT with different prompts for Instagram, TikTok, and Twitter
    """
    prompts = [
        f"Create an engaging Instagram Reels script for {product_name}. The product description is: {description}. The user's script idea requirements are: {script_idea}. {f'Additional context from Twitter: {twitter_content}' if twitter_content else ''} Make it fun, energetic, and include emojis. Focus on visual storytelling and include specific shot suggestions. Keep it under 30 seconds.",
        f"Create a product showcase Instagram Reels script for {product_name}. The product description is: {description}. The user's script idea requirements are: {script_idea}. {f'Additional context from Twitter: {twitter_content}' if twitter_content else ''} Make it educational, include before/after scenarios, and use trending transitions. Keep it under 30 seconds.",
        f"Create a TikTok script for {product_name}. The product description is: {description}. The user's script idea requirements are: {script_idea}. {f'Additional context from Twitter: {twitter_content}' if twitter_content else ''} Make it trendy, include popular music suggestions, and use current social media lingo. Include specific timing cues and transitions. Keep it under 60 seconds.",
        f"Create a behind-the-scenes TikTok script for {product_name}. The product description is: {description}. The user's script idea requirements are: {script_idea}. {f'Additional context from Twitter: {twitter_content}' if twitter_content else ''} Make it authentic, include user testimonials, and use trending sounds. Keep it under 60 seconds.",
        f"Create a Twitter thread script for {product_name}. The product description is: {description}. The user's script idea requirements are: {script_idea}. {f'Additional context from Twitter: {twitter_content}' if twitter_content else ''} Make it concise, engaging, and include relevant hashtags. Break it into 4-5 tweets with a clear narrative flow. Include emojis and attention-grabbing hooks.",
        f"Create a product announcement Twitter thread for {product_name}. The product description is: {description}. The user's script idea requirements are: {script_idea}. {f'Additional context from Twitter: {twitter_content}' if twitter_content else ''} Make it exciting, include user benefits, and use a mix of text and emojis. Break it into 4-5 tweets with a clear call-to-action."
    ]
    
    scripts = []
    
    for i, prompt in enumerate(prompts):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional social media content creator specializing in short-form video and micro-blogging platforms."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            script_content = response.choices[0].message.content
            
            script_type = [
                "Instagram Reels (Engaging)",
                "Instagram Reels (Product Showcase)",
                "TikTok (Trendy)",
                "TikTok (Behind-the-Scenes)",
                "Twitter Thread (Narrative)",
                "Twitter Thread (Product Announcement)"
            ][i]
            
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
