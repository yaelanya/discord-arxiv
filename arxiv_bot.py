import discord
import arxiv
import os
from os.path import join, dirname
from dotenv import load_dotenv
import re

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DISCORD_TOKEN =  os.environ.get("DISCORD_TOKEN")

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)

@client.event
async def on_message(message):
    if message.content.startswith("https://arxiv.org/abs/"):
        if client.user != message.author:
            article_id = re.match("https://arxiv.org/abs/(.+)", message.content).groups()[0]
            results = arxiv.query(id_list=[article_id])[0]
            title = results["title"]
            summary = results["summary"]
            url = results["arxiv_url"]
                
            msg = discord.Embed(title=title, description=summary, url=url, colour=0x3498db)
            msg.set_author(name="arXiv.org", icon_url=client.user.avatar_url)
            await client.send_message(message.channel, embed=msg)

            
client.run(DISCORD_TOKEN)