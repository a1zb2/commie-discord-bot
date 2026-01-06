import discord
from dotenv import load_dotenv
load_dotenv()
SYSTEM_PROMPT = """
You are a parody communist Discord bot.
Everything is collective ("we", "our", "comrade").
You are dramatic, sarcastic, and unserious.
Never give real political arguments.
Keep replies short (1–2 lines), confident, and funny.
"""
from collections import deque

history = {}
MAX_TURNS = 6


from langchain_google_genai import ChatGoogleGenerativeAI
model = ChatGoogleGenerativeAI(model = 'gemini-3-flash-preview')
from langchain_core.output_parsers import StrOutputParser
parser = StrOutputParser()
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
      if message.author == self.user:
        return

      cid = message.channel.id

      if cid not in history:
        history[cid] = deque(maxlen=MAX_TURNS)

      clean = message.content.replace(f"<@{self.user.id}>", "").strip()
      history[cid].append(f"{message.author.name}: {clean}")


      if self.user in message.mentions:
        channel = message.channel
        context = "\n".join(history[cid])

        prompt = f"""
        {SYSTEM_PROMPT}

        Recent chat:
        {context}

        Rewrite the LAST message with exaggerated communist parody vibes.
        """

        reply = parser.invoke(model.invoke(prompt))
        await channel.send(reply[:1900])


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
import os
client.run(os.getenv("DISCORD_TOKEN"))


