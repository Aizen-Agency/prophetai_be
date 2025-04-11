import os
import uuid
from random import choice
from flask import Blueprint, Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from app.models import db
from app.models.userData import UserData
import jwt
from datetime import datetime, timedelta

load_dotenv()

api_scripts = Blueprint("scripts", __name__, url_prefix="")


@api_scripts.route('/generate-scripts', methods=['POST'])
def generate_script():
    try:
        data = request.get_json()
        
        # Validate request data
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        # Extract and validate required fields
        required_fields = ['title', 'description']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"Missing or empty required field: {field}"}), 400

        # Extract data
        title = data['title']
        description = data['description']

        # Generate script variations based on the provided data
        script_variations = [
            {
                'title': f"{title}: Content Creation Revolution (Instagram Reels Copy 1)",
                'content': f"""[Upbeat music starts]
👋 Hey creators! Tired of staring at blank screens?
🤖 Meet {title}, your new content bestie!
💡 {description}
📱 {script_idea}
🎨 Learns your style, sounds like you!
🔍 SEO optimized for more views!
🚀 Boost productivity, save time!
😎 User-friendly, no tech wizardry needed!
🔥 Say bye to writer's block, hello to wow content!
🌟 Try {title} now!
[Call to action: Swipe up to revolutionize your content game!]
#ContentCreation #AIAssistant #{title.replace(' ', '')}""",
                'type': 'copy1'
            },
            {
                'title': f"{title}: Content Creation Revolution (Instagram Reels Copy 2)",
                'content': f"""[Energetic beat drops]
🎭 Content creators, listen up!
😓 Struggling with writer's block?
🚀 Introducing {title}!
⚡ {description}
🧠 Learns your unique style
📊 SEO optimization built-in
⏱️ Save hours on content creation
🌈 Multiple formats, one tool
💪 Empower your creativity
🔥 Stand out in the digital noise
[Visual: "Try {title} Free" button appears]
Don't miss out on the future of content creation!
#{title.replace(' ', '')} #ContentRevolution #CreatorTools""",
                'type': 'copy2'
            },
            {
                'title': f"{title}: Content Creation Revolution (Instagram Reels Copy 3)",
                'content': f"""[Upbeat electronic music]
👀 Attention all content creators!
🤯 Feeling overwhelmed by content demands?
🦸‍♀️ {title} to the rescue!
🎨 {description}
⚡ Lightning-fast creation process
📈 Built-in SEO for maximum reach
🔄 Adapts to your style over time
💡 Never run out of ideas again
🚀 Skyrocket your content strategy
✨ Unlock your creative potential
[Text overlay: "Join the AI content revolution"]
Transform your content game with {title}!
#AIContentCreation #DigitalMarketing #{title.replace(' ', '')}""",
                'type': 'copy3'
            }
        ]

        return jsonify({
            "message": "Scripts generated successfully",
            "scripts": script_variations
        }), 200

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500



@api_scripts.route('/generate-script-idea', methods=['POST'])
def generate_script_idea():
    try:
        data = request.get_json()
        
        # Validate request data
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        # Extract and validate required fields
        required_fields = ['product_name', 'description', 'link', 'script_idea']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"Missing or empty required field: {field}"}), 400

        # Extract data
        product_name = data['product_name']
        description = data['description']
        link = data['link']
        script_idea = data['script_idea']

        # Parse inclusion and exclusion criteria from script_idea
        lines = script_idea.lower().split('\n')
        included_topics = []
        excluded_topics = []

        for line in lines:
            line = line.strip()
            if line.startswith('i want') or line.startswith('include'):
                included_topics.extend(
                    line.replace('i want', '').replace('include', '').strip().split()
                )
            elif line.startswith('i don\'t want') or line.startswith('i do not want') or line.startswith('exclude'):
                excluded_topics.extend(
                    line.replace('i don\'t want', '').replace('i do not want', '').replace('exclude', '').strip().split()
                )

        # Generate script ideas based on the criteria
        script_ideas = []
        base_ideas = [
            {
                'title': f"How {product_name} Revolutionizes Content Creation",
                'content': f"Discover how {product_name} transforms your content creation process with AI-powered tools and features.",
                'focus': ['innovation', 'technology', 'efficiency']
            },
            {
                'title': f"Master Content Creation with {product_name}",
                'content': f"Learn the secrets of professional content creation using {product_name}'s advanced features and capabilities.",
                'focus': ['education', 'tutorial', 'skills']
            },
            {
                'title': f"{product_name}: Your AI Content Assistant",
                'content': f"Meet your new AI-powered content assistant that helps you create engaging content effortlessly.",
                'focus': ['assistant', 'automation', 'productivity']
            },
            {
                'title': f"Content Creation Made Easy with {product_name}",
                'content': f"Simplify your content creation workflow with {product_name}'s intuitive interface and powerful features.",
                'focus': ['simplicity', 'usability', 'workflow']
            },
            {
                'title': f"Boost Your Content Game with {product_name}",
                'content': f"Take your content to the next level with {product_name}'s cutting-edge tools and features.",
                'focus': ['growth', 'improvement', 'results']
            }
        ]

        # Filter and customize ideas based on inclusion/exclusion criteria
        for idea in base_ideas:
            # Check if idea matches inclusion criteria
            if included_topics:
                if not any(topic in idea['content'].lower() or topic in idea['title'].lower() for topic in included_topics):
                    continue

            # Check if idea matches exclusion criteria
            if excluded_topics:
                if any(topic in idea['content'].lower() or topic in idea['title'].lower() for topic in excluded_topics):
                    continue

            # Add product-specific details
            idea['content'] = f"{idea['content']}\n\n{description}\n\nTry it now: {link}"
            script_ideas.append(idea)

        # If no ideas match the criteria, return a default set
        if not script_ideas:
            script_ideas = [{
                'title': f"Discover {product_name}",
                'content': f"{description}\n\nTry it now: {link}",
                'focus': ['general', 'overview']
            }]

        return jsonify({
            "message": "Script ideas generated successfully",
            "ideas": script_ideas,
            "included_topics": included_topics,
            "excluded_topics": excluded_topics
        }), 200

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

        
