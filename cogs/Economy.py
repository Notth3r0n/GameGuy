import discord
from discord.ext import commands
import json
import random
import time
class Economy(commands.Cog):
  def __init__(self, client):
    self.client = client


  @commands.Cog.listener()
  async def on_ready(self):
    time.sleep(0.5)
    print(f"{__name__} has loaded.")

  
  #BALANCE COMMAND
  @commands.command(aliases=["bal"])
  async def balance(self, ctx, member: discord.Member=None):
    
    with open("cogs/eco.json", "r") as f:
      user_eco = json.load(f)
    if member is None:
      member = ctx.author
    elif member is not None:
      member = member

    #check if member has account, if not make one for them
    if str(member.id) not in user_eco:
      user_eco[str(member.id)] = {}
      user_eco[str(member.id)]["Wallet"] = 50
      user_eco[str(member.id)]["Bank"] = 0
      with open("cogs/eco.json", "w") as f:
        json.dump(user_eco, f, indent=4)

    #Outputing balance
    eco_embed = discord.Embed(title=f"{member.name}'s Current Balance", color = discord.Color.blue())
    eco_embed.add_field(name="Wallet:", value=f"{user_eco[str(member.id)]['Wallet']} coins")
    eco_embed.add_field(name="Bank:", value=f"{user_eco[str(member.id)]['Bank']} coins")
    eco_embed.set_footer(text="Want to earn more money? Try playing some games!")
    await ctx.reply(embed=eco_embed)


  #BEG COMMAND
  @commands.command()
  @commands.cooldown(1, 60)
  async def beg(self, ctx):
    with open("cogs/eco.json", "r") as f:
      user_eco = json.load(f)
      
    #check if member has account, if not make one for them
    if str(ctx.author.id) not in user_eco:
      user_eco[str(ctx.author.id)] = {}
      user_eco[str(ctx.author.id)]["Wallet"] = 50
      user_eco[str(ctx.author.id)]["Bank"] = 0

      with open("cogs/eco.json", "w") as f:
        json.dump(user_eco, f, indent=4)

    #Random amount that can be earned or lost
    amount = random.randint(-9,30)

    if amount == -9 or amount == -8 or amount == -7 or amount == -6 or amount == -5:
      await ctx.reply(f"Oh no! You've been robbed of {amount[1]} coins at gunpoint!")

      user_eco[str(ctx.author.id)]["Wallet"] += amount

      with open("cogs/eco.json", "w") as f:
        json.dump(user_eco, f, indent=4)

    elif amount == -4 or amount == -3 or amount == -2 or amount == -1:
      await ctx.reply(f"Oh no! {amount[1]} coins has been stolen!")

      user_eco[str(ctx.author.id)]["Wallet"] += amount

      with open("cogs/eco.json", "w") as f:
        json.dump(user_eco, f, indent=4)

    elif amount == 0:
      await ctx.reply("You've ran out of luck! Nobody gave you coins")

    elif amount == 1:
      await ctx.reply(f"Some kind souls gave you {amount} coin!")

      user_eco[str(ctx.author.id)]["Wallet"] += amount

      with open("cogs/eco.json", "w") as f:
        json.dump(user_eco, f, indent=4)
    else:
      await ctx.reply(f"Some kind souls gave you {amount} coins!")

      user_eco[str(ctx.author.id)]["Wallet"] += amount

      with open("cogs/eco.json", "w") as f:
        json.dump(user_eco, f, indent=4)


  #WORK COMMAND
  @commands.cooldown(1, per=86400)
  @commands.command()
  async def work(self, ctx): 
    with open("cogs/eco.json", "r") as f:
      user_eco=json.load(f)

    #check if member has account, if not make one for them
    if str(ctx.author.id) not in user_eco:       
      user_eco[str(ctx.author.id)] = {}
    
      user_eco[str(ctx.author.id)]["Wallet"] = 50
      user_eco[str(ctx.author.id)]["bank"] = 0
    
      with open("cogs/eco.json", "w") as f: 
        json.dump(user_eco, f, indent=4)

    #randomize amount user earns
    amount=random.randint(100, 308) 
    user_eco[str(ctx.author.id)]["Wallet"] += amount

    eco_embed = discord.Embed(title=f"Great Work!", color = discord.Color.blue())
    eco_embed.add_field(name="You've Earned:", value=f"{amount} coins")
    await ctx.reply(embed=eco_embed)

  
  #DEPOSIT COMMAND
  @commands.command(aliases=['dep'])
  async def deposit(self,ctx,amount:int):
    with open("cogs/eco.json", "r") as f:
      user_eco=json.load(f)

    #check if member has account, if not make one for them
    if str(ctx.author.id) not in user_eco:       
      user_eco[str(ctx.author.id)] = {}
    
      user_eco[str(ctx.author.id)]["Wallet"] = 50
      user_eco[str(ctx.author.id)]["bank"] = 0
    
      with open("cogs/eco.json", "w") as f: 
        json.dump(user_eco, f, indent=4)

    #check if user inputs valid amount
    if amount > user_eco[str(ctx.author.id)]["Wallet"]:
      await ctx.reply("You're not that rich!")
    elif amount<0:
      await ctx.reply("You can't deposit negative amounts of coins!")
    else:
      user_eco[str(ctx.author.id)]["Bank"] += amount
      user_eco[str(ctx.author.id)]["Wallet"] -= amount
      eco_embed = discord.Embed(title="Bank", color = discord.Color.blue())
      eco_embed.add_field(name="You've deposited:", value=f"{amount} coins")
      await ctx.reply(embed=eco_embed)
      with open("cogs/eco.json", "w") as f: 
        json.dump(user_eco, f, indent=4)


  #WITHDRAW COMMAND
  @commands.command(aliases=['wd'])
  async def withdraw(self,ctx,amount:int):
    with open("cogs/eco.json", "r") as f:
      user_eco=json.load(f)

    #check if member has account, if not make one for them
    if str(ctx.author.id) not in user_eco:       
      user_eco[str(ctx.author.id)] = {}
    
      user_eco[str(ctx.author.id)]["Wallet"] = 50
      user_eco[str(ctx.author.id)]["bank"] = 0
    
      with open("cogs/eco.json", "w") as f: 
        json.dump(user_eco, f, indent=4)

    #check if user inputs valid amount
    if amount > user_eco[str(ctx.author.id)]["Bank"]:
      await ctx.reply("You're not that rich!")
    elif amount<0:
      await ctx.reply("You can't withdraw negative amounts of coins!")
    else:
      user_eco[str(ctx.author.id)]["Bank"] -= amount
      user_eco[str(ctx.author.id)]["Wallet"] += amount
      eco_embed = discord.Embed(title="Wallet", color = discord.Color.blue())
      eco_embed.add_field(name="You've withdrawn:", value=f"{amount} coins")
      await ctx.reply(embed=eco_embed)
      with open("cogs/eco.json", "w") as f: 
        json.dump(user_eco, f, indent=4)


  #ERROR HANDLING
  @beg.error
  async def clear_error(sef, ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      await ctx.reply(f"You are begging too much! Retry after {round(error.retry_after, 2)} seconds.")
  @work.error
  async def clear_error(sef, ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      await ctx.reply(f"You are working too much! Retry after {(round(error.retry_after, 2))/60} minutes.")
async def setup(client):
  await client.add_cog(Economy(client))
