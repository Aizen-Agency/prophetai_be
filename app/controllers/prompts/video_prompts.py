def get_video_prompts(product_name, description, script_idea, twitter_content=None):
    """
    Returns a list of video prompts for different video types
    """
    prompts = [
        # Prompt 1: Talking Head Video
        '''
        I'm providing you with:
        1. A speech-to-text transcript of my thoughts on a trending post.
        2. A writing template that reflects my preferred style.
        3. The original post's copy or video script for additional context.

        Your task is to rewrite my thoughts into a polished, engaging, and structured video script that mirrors the writing template. The final script should maximize engagement, maintain strong pacing, and feel natural. Keep it concise—ideally around 180 words and make it accessible to a 17 year old. **Avoid sentence fragments or one-word rhetorical questions (e.g., 'China?') in the final script.**
        • Do not summarize the original post. Instead, focus on my perspective.
        • Ensure the script is compelling, concise, and structured for virality.

        Inputs:

        • Transcript:

        INSERT TRANSCRIPT
        Writing Template:

        Within the next 10 years, AI won't just be something you interact with—it'll be something that perceives the world *as you do.*

        Meta just announced Aria Gen 2, AR glasses designed to bridge the gap between human and machine perception. These aren't just smart glasses. They're always-on, data-hungry sensors tracking your every move, your gaze, even your *heartbeat.*

        The *good* part? This tech could revolutionize AI training. By capturing how skilled professionals move and interact, we're essentially teaching robots to take over complex tasks. A chef, a surgeon, a carpenter—wear these glasses, and the AI learns directly from you. It's a leap forward in automation.

        The *bad* part? This is Meta. A company built on centralized data collection now has a device that *sees* everything you see and *knows* everything you feel. They promise privacy safeguards, but is your data processed on-device or sent to Meta's servers? If it's the latter, privacy is already lost.

        So ask yourself—do you want AI that serves *you*? Or one where you're just feeding it for free?

        • Original Post Copy:

        INSERT ORIGINAL POST COPY HERE
        ''',
        
        # Prompt 2: Fake Podcast
        '''
        I'm providing you with:
        1. A speech-to-text transcript of my thoughts on a trending post.
        2. A writing template that reflects my preferred style.
        3. The original post's copy or video script for additional context.

        Your task is to rewrite my thoughts into a polished, engaging, and structured short-form podcast script that mirrors the writing template. The final script should be tight, fast-paced, and engaging, keeping the energy high to maximize virality and start the script as if the speaker is in the middle of a statement that is extremely strong as a hook. Keep it within 15-30 seconds—no fluff, just impact.
        • Do not summarize the original post. Instead, focus on my perspective.
        • Do not ask questions in the script like "The Truth?", just get to the point
        • Keep the script punchy, conversational, and to the point.
        • No pauses, stage directions, or filler words—just clean, spoken words that flow naturally.

        Inputs:

        • Transcript:

        INSERT FOUNDER TRANSCRIPT
        Writing Template:

        If Musk was really trying to find, he wouldn't be hiring programmers
        He'd be hiring forensic accountants
        Financial records inside of a single company are incredibly difficult to piece together, I had a friend who's employee stole a bunch of money from him and it took a ton of effort to figure out exactly what money was stolen when
        How are 19 year old programmers who have no real experience in finance supposed to figure this out?
        The answer is they were never supposed to figure it out
        Their job from the beginning was to go in, cut the programs that Elon and Trump weren't politically aligned with and call it fraud or waste, while NEVER bringing forth a criminal case showing actual fraud
        That would be a huge win for Trump if he could supply one case, but he won't
        Because again it was never about that.

        • Original Post Copy:

        INSERT ORIGINAL POST COPY
        ''',
        
        # Prompt 3: Reaction Video (Mid Roll)
        '''
        Please create a reaction video script optimized for YouTube Shorts that maximizes engagement and virality. Do not include any section markers or script instructions, only the words that the speaker needs to read. The script should be structured as follows:

        Hook/Intro (10-15 seconds):

        • Start with a bold, polarizing, or emotionally compelling statement that immediately grabs attention.

        • The goal is to provoke curiosity, outrage, or strong interest within the first few seconds.

        Show Clip (5-10 seconds):

        • Insert a placeholder for the video clip: [SHOW CLIP].

        • The clip should provide enough context while keeping the pacing fast.

        Commentary (20-40 seconds):

        • Analyze, critique, or deconstruct the clip in an insightful, provocative, or humorous way.

        • Maintain a high-energy delivery and avoid drawn-out explanations.

        • If applicable, highlight contradictions, logical fallacies, or unintended consequences.

        • Use rhetorical questions, sarcasm, and analogies to enhance engagement.

        Closing (Optional, but recommended):

        • End with a thought-provoking statement, rhetorical question, or cliffhanger to drive audience interaction.
        Example: *"So, what do you think—are they onto something, or is this just straight-up delusion?"*

        Additional Guidelines for Output Quality:

        • Brevity & Impact: Keep sentences short and punchy.

        • Clarity & Flow: Ensure smooth transitions between sections.

        • Conversational Tone: Write in a way that feels natural for spoken delivery.

        • Engagement Hooks: End with a question or challenge to encourage comments.

        Example Script (Template):

        Intro (Hook):

        *"So it turns out that many MAGA voters would rather vote for Vladimir Putin than Kamala Harris. Wild, right? Well, here's why."*

        Show Clip:

        *[SHOW CLIP]*

        Commentary:

        *"So, here's their logic: Kamala Harris represents the deep state. A shadowy network controlled by—wait for it—Jewish bankers. They think this cabal runs the world, profits off wars, and is using Ukraine to undermine Russia."*

        *"Meanwhile, Putin is their hero—a defender of Christianity and traditional values. But there's just one problem: in Putin's America, there's no free speech, no guns, no bill of rights, and the government runs the economy like a mafia. Everything MAGA claims to hate, yet here they are supporting it."*
        *"This is what happens when your biggest enemy is an invisible conspiracy you can't disprove. The boogeyman keeps shifting, and suddenly your positions make zero sense."*

        *"Let me know what you think—does this logic track, or is this just straight-up delusion?"*

        Final Instructions:

        Use this exact format to generate a reaction script. Below are the necessary inputs:

        1. My Audio Transcript for Reference (So you can match my style):

        **[INSERT YOUR PREVIOUS AUDIO TRANSCRIPT HERE]**

        2. Trending Video Transcript (So you have extra content to give you additional context about what is being discussed:

        **[INSERT TRENDING VIDEO TRANSCRIPT HERE]**
        ''',
        
        # Prompt 4: Reaction Video (End Roll)
        '''
        Please create a reaction video script optimized for YouTube Shorts that maximizes engagement and virality. The script should follow this format:

        Hook/Intro (10-15 seconds):

        • Start with a bold, polarizing, or emotionally compelling statement to immediately grab attention.

        • The goal is to provoke curiosity, outrage, or strong interest within the first few seconds.

        • The transition into the trending clip should feel organic and seamless, naturally setting up the viewer for what's about to happen.

        Show Clip (For the last part of the video):

        • Insert a placeholder for the video clip: [SHOW CLIP]

        • The clip should play until the video ends without further interruptions.

        Additional Guidelines for Output Quality:

        • Brevity & Impact: Keep the intro short and punchy with high-energy delivery.

        • Clarity & Flow: Ensure a smooth transition from the intro into the clip.

        • Conversational Tone: Write in a way that feels natural for spoken delivery.

        • Engagement Hooks: The intro should create curiosity so viewers stay for the full clip.

        Example Script (Template):

        Intro (Hook):

        *"The thing I'm about to show you is maybe the most terrifying video of a robot I've ever seen."*

        *"This thing can run 10 meters a second."*
        *"Which means that if you were at one end of a football field and it was on the other, it could reach you within 10 seconds."*

        *"Imagine what tech like this does for our military, Russia's military, and China's military."*

        *"Take a look."*

        Show Clip:

        [SHOW CLIP — The trending clip plays for the last part of the video.]

        Final Instructions:

        Use this exact format to generate a reaction script. Below are the necessary inputs:

        1. My Audio Transcript for Reference (So ChatGPT Matches My Style):

        [INSERT YOUR PREVIOUS AUDIO TRANSCRIPT HERE]

        2. Trending Video Transcript (So ChatGPT Can React to It Properly):

        [INSERT TRENDING VIDEO TRANSCRIPT HERE]
        ''',
        
        # Prompt 5: Video Title
        "Please give me 10 possible titles for this script that are optimized for social media and grab a viewers attention, and keep it under 46 characters"
    ]
    
    return prompts
