import discord
from discord.ext import commands
import json
import random
import time

class Fishing(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        time.sleep(0.5)
        print(f"{__name__} has loaded.")


    @commands.command()
    async def fish(self, ctx):
        with open("cogs/inven.json", "r") as f:
            user_inven = json.load(f)

        bag = user_inven.get(str(ctx.author.id), {}).get("Bag", [])
        #check if user has a fishing rod
        if (
            "common fishing rod" in bag
            or "uncommon fishing rod" in bag
            or "rare fishing rod" in bag
            or "epic fishing rod" in bag
            or "legendary fishing rod" in bag
            or "mythic fishing rod" in bag
        ):
            #chances of catching fish for each fishing rod tier
            if "common fishing rod" in bag:
                fish_names = ["Trash", "Trash", "Bass", "Trash", "Trash", "Salmon", "Trash", "Trash", "Trout", "Trash", "Trash", "Catfish", "Trash", "Tuna", "Trash"]
            elif "uncommon fishing rod" in bag:
                fish_names = ["Trash", "Bass", "Trash", "Salmon", "Trash", "Trash", "Trout", "Trash", "Trash", "Catfish", "Trash", "Tuna", "Trash"]
            elif "rare fishing rod" in bag:
                fish_names = ["Bass", "Trash", "Salmon", "Trash", "Trash", "Trout", "Trash", "Trash", "Catfish", "Trash", "Tuna"]
            elif "epic fishing rod" in bag:
                fish_names = ["Bass", "Salmon", "Trash", "Trash", "Trout", "Trash", "Catfish", "Trash", "Tuna"]
            elif "legendary fishing rod" in bag:
                fish_names = ["Bass", "Salmon", "Trash", "Trout", "Trash", "Catfish", "Tuna"]
            elif "mythic fishing rod" in bag:
                fish_names = ["Bass", "Salmon", "Trout", "Catfish", "Tuna"]

            caught_fish = random.choice(fish_names)
            if caught_fish == "Trash":
                fish_value = 0
            else:
                fish_value = random.randint(10, 50)

            if str(ctx.author.id) not in user_inven:
                user_inven[str(ctx.author.id)] = {}
                user_inven[str(ctx.author.id)]["Bag"] = []
                user_inven[str(ctx.author.id)]["Fish Bag"] = []

            if caught_fish == "Trash":
                trash_em = discord.Embed(title="You've caught trash!", description="It is worth nothing")
                await ctx.reply(embed=trash_em)
            else:
                user_inven[str(ctx.author.id)]["Fish Bag"].append({"name": caught_fish, "value": fish_value})
                with open("cogs/inven.json", "w") as f:
                    json.dump(user_inven, f, indent=4)

                caught_em = discord.Embed(title=f"You caught a {caught_fish}", description=f"It is worth {fish_value} coins!", color=discord.Color.blurple())
                await ctx.reply(embed=caught_em)
        else:
            notrod_em = discord.Embed(title='Error!', description='You have not bought a fishing rod!')
            await ctx.reply(embed=notrod_em)

      #SELL Command
    @commands.command()
    @commands.cooldown(1, 300)
    async def sellfish(self, ctx):
        with open("cogs/inven.json", "r") as f:
            user_inven = json.load(f)
        with open("cogs/eco.json", "r") as f:
            user_eco = json.load(f)

        if str(ctx.author.id) not in user_inven or "Fish Bag" not in user_inven[str(ctx.author.id)]:
            no_em = discord.Embed(title='Error!', description="You don't have any fish to sell.")
            await ctx.reply(embed=no_em)
            return

        total_coins = 0
        for fish_item in user_inven[str(ctx.author.id)]["Fish Bag"]:
            total_coins += fish_item["value"]

        user_eco[str(ctx.author.id)]["Wallet"] += total_coins

        user_inven[str(ctx.author.id)]["Fish Bag"] = []
        with open("cogs/inven.json", "w") as f:
            json.dump(user_inven, f, indent=4)
        with open("cogs/eco.json", "w") as f:
            json.dump(user_eco, f, indent=4)

        sold_em = discord.Embed(title='You sold all your fish', description=f"You earned {total_coins} coins!")
        await ctx.reply(embed=sold_em)

    @fish.error
    async def clear_error(sef, ctx, error):
      if isinstance(error, commands.CommandOnCooldown):
        await ctx.reply(f"You are fishing too much! Retry after {round(error.retry_after, 2)/60} minutes.")
        
async def setup(client):
    await client.add_cog(Fishing(client))
