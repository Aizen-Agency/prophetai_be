SHORT_SCRIPT_IDEA_PROMPT = """
Rewrite my transcript into a polished, engaging, and fast-paced X post using the provided template's style as a thread. Each section of the thread must be 280 characters or less and should always end with slash number as found in the template, except for the last section of the thread which should end as slash end

• Keep it informal, direct, and spontaneous, like someone quickly typing out their thoughts.
• Remove filler words, ums, uhs, and repeated phrases, but keep the natural flow of speech so it doesn't feel too polished.
• Use commas and periods casually to match the informal, on-the-fly writing style.
• Match the structure and tone of the template while preserving my original argument.
• Make sure the post sparks discussion and feels like it belongs on X.

Video Script:

{script}

Raw Transcript:

{transcript}

Template to Mimic:

Zelensky has thanked Trump, Congress, and the American people many times.

But let's be clear: when Trump and Vance said that THEY are trying to help Ukraine right now, and need to be thanked for the work personally, there are reasons to wonder.  1/ THREAD

1. Team Trump has told Ukraine that they have to give up territory to Russia. Zelenskyy should thank them for that? 2/
2. Trump has told Ukraine that they cannot join NATO. Zelenskyy should thank them for that? 3/

3/ Team Trump has said that if there is an international peacekeeping force in Ukraine, American soldiers will not participate.  Zelenskyy should thank them for that? 4/

4/ Team Trump has said that they plan to reduce the number of U.S. soldiers deployed in Europe. That's a huge gift to Putin. Zelenskyy should thank them for that?  5/

5/. Zelenskyy has been told that Ukraine must hold new presidential elections before negotiations to end the war start.  Zelenskyy should thank them for that? 6/

1. U.S.-Russia relations were formally restarted without any preconditions at a meeting between Secretary of State Rubio and Foreign Minister Lavrov in Saudi Arabia. 7/

7/  Trump officials have hinted at sanctions relief for Russia. 8/
8/ Trump invited Russia to rejoin the G7.  9/

9/ The United States voted "No" on a UN resolution condemning Russia's invasion of Ukraine. In doing so, Trump broke ranks with American democratic allies and sided with Russia, Belarus, North Korea, and other dictatorships. Zelenskyy should thank them for that? 10/

The aid that Vance demanded Zelensky thank him for today?  Vance voted against it.  The GOP held it it up for 6 months. Trump said that "stupid" Biden gave it. 11/

So what exactly should Zelenskyy be thanking Trump/Vance for?  Congress, yes. The American taxpayer, yes. But Trump has not done anything for Ukraine yet. All Trump team does is offer gifts to Putin. It's the Russian dictator who they should be demanding thanks from. 12/ END
"""

LONG_SCRIPT_IDEA_PROMPT = """
Rewrite my transcript into a polished, engaging, and fast-paced X post using the provided template's style.
• Keep it informal, direct, and spontaneous, like someone quickly typing out their thoughts.
• Remove filler words, ums, uhs, and repeated phrases, but keep the natural flow of speech so it doesn't feel too polished.
• Use commas and periods casually to match the informal, on-the-fly writing style.
• Match the structure and tone of the template while preserving my original argument.
• Make sure the post sparks discussion and feels like it belongs on X.

Video Script:

{script}

Raw Founder Transcript:

{transcript}

Template to Mimic:

There is a strong argument that Ukraine is THE climactic battle of the Thucydides Trap.
That is: the big war between the US and China is actually between their proxies Ukraine and Russia.
And this settlement — to this war — determines the next world order.
Because there won't be a fight in Taiwan if NATO is defeated in Ukraine. Taiwan will just surrender to China because they know they won't get reliable Western military support.
And so will everyone else.
So, this may be the decisive moment when terms get negotiated with the China/Russia group for the next however many years.
That means that even if you think Ukraine was a disaster and Zelensky is a dummy, you don't want NATO to be catastrophically defeated in Kiev like it was in Afghanistan.
That would be bad for Democrats, Republicans, Europeans, Japanese — just about everyone under the US security umbrella.
Instead you want the best possible outcome to this terrible war, under the circumstances.
Because the West may already have fallen into the Thucydides Trap. And if so, it should very carefully think about whether it can get out.
"""

__all__ = ['SHORT_SCRIPT_IDEA_PROMPT', 'LONG_SCRIPT_IDEA_PROMPT']
