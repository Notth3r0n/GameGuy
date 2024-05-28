import discord
from discord.ext import commands
import random
import json
import time
class rps(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.choices = ['rock', 'paper', 'scissors']

    @commands.Cog.listener()
    async def on_ready(self):
        time.sleep(0.5)
        print(f"{__name__} has loaded.")

    @commands.command()
    async def rps(self, ctx, choice: str):
        choice = choice.lower()
        user_id = str(ctx.author.id)
        with open("cogs/eco.json", "r") as f:
          user_eco=json.load(f)
        #check if choice is made
        if choice == '':
          await ctx.reply("Please enter either 'rock', 'paper', or 'scissors'( !rps [choice] )")
        #check if choice is valid
        if choice not in self.choices:
            await ctx.reply("Invalid choice! Please choose either 'rock', 'paper', or 'scissors'.")
            return
            
        #randomizing bots choice
        bot_choice = random.choice(self.choices)
        result = self.get_result(choice, bot_choice)
        
        #win condition
        if result == 'win':
            win_em = discord.Embed(title='You Win!', description=f'You chose **{choice}**, and I chose **{bot_choice}**.')
            win_em.add_field(name='', value='5 coins have been added to your wallet')
            user_eco[user_id]["Wallet"] += 5
            await ctx.reply(embed=win_em)
            with open("cogs/eco.json", "w") as f: 
                json.dump(user_eco, f, indent=4)
        #lose condition
        elif result == 'lose':
            lose_em = discord.Embed(title='You Lose!', description=f'You chose **{choice}**, and I chose **{bot_choice}**.')
            lose_em.add_field(name='',value='1 coin has been deducted from your wallet')
            user_eco[user_id]["Wallet"] -= 1
            await ctx.reply(embed=lose_em)
            with open("cogs/eco.json", "w") as f: 
                json.dump(user_eco, f, indent=4)
        #tie condition
        else:
            tie_em = discord.Embed(title='Tie!', description=f'You chose **{choice}**, and I chose **{bot_choice}**.')
            await ctx.reply(embed=tie_em)

    #getting result
    def get_result(self, user_choice, bot_choice):
        if user_choice == bot_choice:
            return 'tie'
        elif (user_choice == 'rock' and bot_choice == 'scissors') or (user_choice == 'paper' and bot_choice == 'rock') or (user_choice == 'scissors' and bot_choice == 'paper'):
            return 'win'
        else:
            return 'lose'

async def setup(client):
  await client.add_cog(rps(client))
