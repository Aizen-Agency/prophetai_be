SHORT_SCRIPT_IDEA_PROMPT = """
Generate 10 unique and engaging script ideas for a product called '{product_name}'.

Product Description: {description}
User's Script Idea: {script_idea}
Twitter Content Context: {twitter_content}

Each idea should:
1. Be written in a fast-paced, informal, Twitter thread style.
2. Be creative and spontaneous, as if someone is quickly typing out thoughts.
3. Spark discussion and resemble real posts on X (Twitter).
4. Be split into short 280-character chunks with a "1/", "2/", ... and end with "END/".

Return a valid JSON object in this format:
{
  "scriptIdeas": [
    {
      "title": "Catchy Title",
      "content": "Formatted Twitter-style script here",
      "focus": "Key theme or angle of the script"
    }
  ]
}
"""

LONG_SCRIPT_IDEA_PROMPT = """
You are a creative content strategist. Your job is to generate 10 long-form and engaging script ideas for a product called '{product_name}'.

Product Description: {description}
User's Script Idea: {script_idea}
Twitter Content Context: {twitter_content}

Each idea must:
1. Be suitable for long-form content (e.g., YouTube, TikTok, or blog posts)
2. Include storytelling, emotional hooks, and compelling narratives
3. Highlight the product's key features and benefits
4. Be engaging and have viral potential
5. End with a strong call-to-action

Return ONLY valid JSON in this exact format:

{
  "scriptIdeas": [
    {
      "title": "Catchy Title",
      "content": "Long-form script content here...",
      "focus": "Main theme or strategy"
    }
  ]
}

⚠️ Do NOT include any markdown, explanations, or text outside the JSON object. ONLY return valid JSON.
"""


__all__ = ['SHORT_SCRIPT_IDEA_PROMPT', 'LONG_SCRIPT_IDEA_PROMPT']
