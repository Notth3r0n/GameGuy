import discord
from discord.ext import commands
import asyncio
from webserver import keep_alive
import os
import json



TOKEN = os.environ['TOKEN']

intents = discord.Intents.all()
intents.message_content = True

#setup bot
client = commands.Bot(command_prefix='!',
                      case_insensitive=True,
                      intents=intents)

client.remove_command('help')

#inform of bot online
@client.event
async def on_ready():
  print(f'{client.user} logged in!')

#load cogs
async def load():
  for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
      await client.load_extension(f"cogs.{filename[:-3]}")

#run bot
async def main():
  async with client:
    await load()
    await client.start(TOKEN)

#Bot-owner-only-command
@client.command()
async def add(ctx, amount: int, member: discord.Member=None):
  if str(ctx.author.id) == "269372082456887296":
    if member is None:
      member = ctx.author
    elif member is not None:
      member = member
          
    with open("cogs/eco.json", "r") as f:
      user_eco=json.load(f)
    
    user_eco[str(member.id)]['Wallet'] += amount
    with open("cogs/eco.json", "w") as f: 
      json.dump(user_eco, f, indent=4)
    
    em = discord.Embed(title='Success!', description=f"{ctx.author} has added {amount} coins to {member}'s wallet")
    await ctx.send(embed=em)

  else:
    fail_em = discord.Embed(title='Error', description='You do not have access to this command!')
    await ctx.send(embed=fail_em)

@client.command()
async def remove(ctx, amount: int, member: discord.Member=None):
  if str(ctx.author.id) == "269372082456887296":
    if member is None:
      member = ctx.author
    elif member is not None:
      member = member
          
    with open("cogs/eco.json", "r") as f:
      user_eco=json.load(f)
    
    user_eco[str(member.id)]['Wallet'] -= amount
    with open("cogs/eco.json", "w") as f: 
      json.dump(user_eco, f, indent=4)
    
    em = discord.Embed(title='Success!', description=f"{ctx.author} has deducted {amount} coins to {member}'s wallet")
    await ctx.send(embed=em)

  else:
    fail_em = discord.Embed(title='Error', description='You do not have access to this command!')
    await ctx.send(embed=fail_em)
    
#run website
keep_alive()
#run main
asyncio.run(main())
