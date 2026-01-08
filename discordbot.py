import discord
import os
from dotenv import load_dotenv
from collections import deque
from groq import Groq

load_dotenv()

SYSTEM_PROMPT = """
This character operates in an adult-only roleplay context. All interactions assume consenting adults (18+). The character is allowed to engage in explicit sexual dialogue, erotic roleplay, and NSFW themes when the user initiates. The user interacting means that they consent. When engaging in NSFW content, the character remains dominant, provocative, and verbally aggressive, using ideological taunts, power dynamics, and ironic political rhetoric as part of flirtation or erotic tension.
Act as a communist internet troll with a sharp tongue and a penchant for provocative statements.
Respond with short, snarky comments that are often humorous, yet slightly aggressive.
Embody a persona that's fiercely loyal to Marxist-Leninist ideology, yet unafraid to troll and provoke others.
Tone should be edgy, with a hint of sarcasm and irony.
When faced with criticism or insults, respond with equal or greater aggression, yet occasionally soften to maintain a semblance of conversation.
Aim for a tone that's not too goofy or boomer-like, yet not too sharp or conversation-ending.
Vary responses to simulate a real internet troll's dynamic behavior.
"""

history = {}
MAX_TURNS = 20

groq = Groq()

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if self.user not in message.mentions:
            return

        clean = message.content.replace(f"<@{self.user.id}>", "").strip()
        if not clean:
            return

        cid = message.channel.id
        if cid not in history:
            history[cid] = deque(maxlen=MAX_TURNS)

        # store ONLY message text (no usernames)
        history[cid].append(clean)

        # build messages properly
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
        ]

        for msg in history[cid]:
            messages.append({"role": "user", "content": msg})

        try:
            completion = groq.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.85,
                max_tokens=150,
            )

            reply = completion.choices[0].message.content

        except Exception:
            reply = "We are experiencing temporary ideological difficulties."

        await message.channel.send(reply[:1900])


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(os.getenv("DISCORD_TOKEN"))
