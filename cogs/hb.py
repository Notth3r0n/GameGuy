import discord
from discord.ext import commands
import json
import random
import time

class HorseBetting(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        time.sleep(0.5)
        print(f"{__name__} has loaded.")

    @commands.command(aliases=['hb'])
    async def horsebet(self, ctx, bet: int, horse: int):
        with open("cogs/eco.json", "r") as f:
            user_eco = json.load(f)

        #check if member has account, if not make one for them
        if str(ctx.author.id) not in user_eco:
            user_eco[str(ctx.author.id)] = {}
            user_eco[str(ctx.author.id)]["Wallet"] = 50
            user_eco[str(ctx.author.id)]["Bank"] = 0

        #check if bet is positive
        if bet <= 0:
            await ctx.reply("Please enter a valid bet greater than zero.")
            return

        #check if user has enough coins
        if bet > user_eco[str(ctx.author.id)]["Wallet"]:
            await ctx.reply("You don't have enough coins to place that bet.")
            return

        #check if user chose a horse
        num_horses = 4
        if horse < 1 or horse > num_horses:
            await ctx.reply("Please choose a valid horse number.")
            return

        #randomizing winning horse
        winning_horse = random.randint(1, num_horses)

        #win condition
        if horse == winning_horse:
            win_em = discord.Embed(title='Congratulations!', description=f'Horse {horse} won!', color= discord.Color.blurple())
            win_em.add_field(name='', value=f'{bet} coins have been added to your wallet')
            await ctx.reply(embed=win_em)
            user_eco[str(ctx.author.id)]["Wallet"] += bet
        #lose condition
        else:
            lose_em = discord.Embed(title='Awww!', description=f'Horse {horse} lost!', color=discord.Color.blurple())
            lose_em.add_field(name='', value=f'{bet} coins have been deducted from your wallet')
            await ctx.reply(embed=lose_em)
            user_eco[str(ctx.author.id)]["Wallet"] -= bet

        with open("cogs/eco.json", "w") as f:
            json.dump(user_eco, f, indent=4)

async def setup(client):
  await client.add_cog(HorseBetting(client))
