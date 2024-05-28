import discord
from discord.ext import commands
from requests import get
import json
import random

class meme(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} has loaded.")

    @commands.command()
    async def meme(self, ctx):
      async with ctx.channel.typing():
        content = ""
        choice = random.randint(1,3)
        if choice == 1:
          content = get("https://meme-api.com/gimme/comedyheaven").text
        elif choice == 2:
          content = get("https://meme-api.com/gimme/metal_me_irl").text
        elif choice == 3:
          content = get("https://meme-api.com/gimme/MemeEconomy").text
        
        data = json.loads(content)
        meme = discord.Embed(title=f"{data['title']}", color = discord.Color.blurple()).set_image(url=f"{data['url']}")
        await ctx.reply(embed=meme)
  


async def setup(client):
    await client.add_cog(meme(client))