def get_video_prompts(product_name, description, script_idea, transcript):
    """
    Returns a list of video prompts for different video types
    """
    prompts = [
        # Prompt 1: Talking Head Video
        f'''
        I'm providing you with:
        1. A speech-to-text transcript of my thoughts on a trending post.
        2. A writing template that reflects my preferred style.
        3. The original post's copy or video script for additional context.

        Your task is to rewrite my thoughts into a polished, engaging, and structured video script that mirrors the writing template. The final script should maximize engagement, maintain strong pacing, and feel natural. Keep it concise—ideally around 180 words and make it accessible to a 17 year old. **Avoid sentence fragments or one-word rhetorical questions (e.g., 'China?') in the final script.**
        • Do not summarize the original post. Instead, focus on my perspective.
        • Ensure the script is compelling, concise, and structured for virality.
        • DO NOT include the writing template in your response.
        • IMPORTANT: Provide ONLY the final script text without any formatting, section markers, or instructions. The output should be ready for direct voicing by an avatar.

        Inputs:

        • Product/Topic:

        INSERT TRANSCRIPT

        • Script Idea:

        {script_idea if script_idea else "No script idea provided"}

        Writing Template:

        Within the next 10 years, AI won't just be something you interact with—it'll be something that perceives the world *as you do.*

        Meta just announced Aria Gen 2, AR glasses designed to bridge the gap between human and machine perception. These aren't just smart glasses. They're always-on, data-hungry sensors tracking your every move, your gaze, even your *heartbeat.*

        The *good* part? This tech could revolutionize AI training. By capturing how skilled professionals move and interact, we're essentially teaching robots to take over complex tasks. A chef, a surgeon, a carpenter—wear these glasses, and the AI learns directly from you. It's a leap forward in automation.

        The *bad* part? This is Meta. A company built on centralized data collection now has a device that *sees* everything you see and *knows* everything you feel. They promise privacy safeguards, but is your data processed on-device or sent to Meta's servers? If it's the latter, privacy is already lost.

        So ask yourself—do you want AI that serves *you*? Or one where you're just feeding it for free?
        ''',
        
        # Prompt 2: Fake Podcast
        f'''
        I'm providing you with:
        1. A speech-to-text transcript of my thoughts on a trending post.
        2. A writing template that reflects my preferred style.
        3. The original post's copy or video script for additional context.

        Your task is to rewrite my thoughts into a polished, engaging, and structured short-form podcast script that mirrors the writing template. The final script should be tight, fast-paced, and engaging, keeping the energy high to maximize virality and start the script as if the speaker is in the middle of a statement that is extremely strong as a hook. Keep it within 15-30 seconds—no fluff, just impact.
        • Do not summarize the original post. Instead, focus on my perspective.
        • Do not ask questions in the script like "The Truth?", just get to the point
        • Keep the script punchy, conversational, and to the point.
        • No pauses, stage directions, or filler words—just clean, spoken words that flow naturally.
        • DO NOT include the writing template in your response.
        • IMPORTANT: Provide ONLY the final script text without any formatting, section markers, or instructions. The output should be ready for direct voicing by an avatar.

        Inputs:

        • Product/Topic:

        INSERT FOUNDER TRANSCRIPT

        • Script Idea:

        {script_idea if script_idea else "No script idea provided"}

        Writing Template:

        If Musk was really trying to find, he wouldn't be hiring programmers
        He'd be hiring forensic accountants
        Financial records inside of a single company are incredibly difficult to piece together, I had a friend who's employee stole a bunch of money from him and it took a ton of effort to figure out exactly what money was stolen when
        How are 19 year old programmers who have no real experience in finance supposed to figure this out?
        The answer is they were never supposed to figure it out
        Their job from the beginning was to go in, cut the programs that Elon and Trump weren't politically aligned with and call it fraud or waste, while NEVER bringing forth a criminal case showing actual fraud
        That would be a huge win for Trump if he could supply one case, but he won't
        Because again it was never about that.
        ''',
        
        # Prompt 3: Reaction Video (Mid Roll)
        f'''
        I'm providing you with:
        1. A product/topic: "{product_name}"
        2. A description: "{description}"
        3. A script idea for context: "{script_idea if script_idea else 'No script idea provided'}"
        4. Trending content for reference

        Your task is to create a reaction video script optimized for YouTube Shorts that maximizes engagement and virality. The script should follow a reaction video format with a hook, commentary on a video clip, and a closing.
        • Start with a bold, polarizing, or emotionally compelling statement that immediately grabs attention
        • Include a [SHOW CLIP] marker where the video clip would be inserted
        • Provide insightful, provocative commentary about the topic/product
        • End with a thought-provoking statement or question to drive audience interaction
        • Keep sentences short and punchy with high-energy delivery
        • Write in a way that feels natural for spoken delivery
        • DO NOT include any section markers or script instructions in your final output
        • DO NOT include the example template in your response
        • IMPORTANT: Provide ONLY the final script text ready for direct voicing by an avatar

        Example Script Format (DO NOT COPY THIS EXACTLY):
        *"Hook statement that grabs attention."*
        [SHOW CLIP]
        *"Commentary about what was shown in the clip, analyzing or providing insight."*
        *"More commentary with some rhetorical questions or points that provoke thought."*
        *"Closing statement that encourages viewer engagement."*

        Inputs:

        • Product/Topic:
        {product_name}

        • Description:
        {description}

        • Script Idea:
        {script_idea if script_idea else "No script idea provided"}

        • Trending Content:
        **[INSERT TRENDING VIDEO TRANSCRIPT HERE]**
        ''',
        
        # Prompt 4: Reaction Video (End Roll)
        f'''
        I'm providing you with:
        1. A product/topic: "{product_name}"
        2. A description: "{description}"
        3. A script idea for context: "{script_idea if script_idea else 'No script idea provided'}"
        4. Trending content for reference

        Your task is to create a reaction video script optimized for YouTube Shorts that maximizes engagement and virality. This should be structured as an "end roll" reaction where your commentary comes after showing the clip.
        • Start with a bold, polarizing, or emotionally compelling statement to immediately grab attention
        • Keep the intro short and punchy with high-energy delivery
        • Include a [SHOW CLIP] marker where the video clip would be inserted
        • After the clip marker, provide insightful, provocative commentary
        • End with a thought-provoking statement or question to drive audience interaction
        • Write in a way that feels natural for spoken delivery
        • DO NOT include any section markers or script instructions in your final output
        • DO NOT include the example script in your response
        • IMPORTANT: Provide ONLY the final script text without any formatting, section markers, or instructions. The output should be ready for direct voicing by an avatar.

        Inputs:

        • Product/Topic:
        {product_name}
        
        • Description:
        {description}

        • Script Idea:
        {script_idea if script_idea else "No script idea provided"}

        • Trending Content:
        [INSERT TRENDING VIDEO TRANSCRIPT HERE]
        ''',
        
        # Prompt 5: Video Title
        f"Please give me 10 possible titles for a video about '{product_name}' that are optimized for social media and grab a viewer's attention. Keep each title under 46 characters. Script idea: {script_idea if script_idea else 'No script idea provided'}"
    ]
    
    return prompts
