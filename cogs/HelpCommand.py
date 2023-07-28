import discord
from discord.ext import commands

class HelpCommand(commands.Cog):
  def __init__(self, client):
    self.client = client


  @commands.Cog.listener()
  async def on_ready(self):
    print(f"{__name__} has loaded.")

  @commands.command()
  async def help(self,ctx, cat: str=None):
    #check if category specified
    if cat == None:
      cat_em = discord.Embed(title="Help Command", color=discord.Color.blurple())
      cat_em.add_field(name='Economy', value='Do !help economy for a list of economy commands')
      cat_em.add_field(name='Shop', value='Do !help shop for a list of shop commands')
      cat_em.add_field(name='Games', value='Do !help games for a list of game commands')
      cat_em.add_field(name='Fish', value='Do !help fish for a list of fish commands')
      await ctx.send(embed=cat_em)

    #output when economy cat is specified
    elif cat.lower() == 'economy':
      eco_embed = discord.Embed(title='Economy Commands List', color=discord.Color.blurple())
      
      eco_embed.add_field(name='Balance [user]', value='Checks users balance // aliases: bal', inline=False)
      eco_embed.add_field(name='Deposit [amount]', value='Deposit cash into your bank // aliases: dep', inline=False)
      eco_embed.add_field(name='Withdraw [amount]', value='Withdraw cash from your bank // aliases: wd', inline=False)
      eco_embed.add_field(name='Beg', value='Earn OR lose a small amount of coins', inline=False)
      eco_embed.add_field(name='Work', value='Earn coins once a day', inline=False)
  
      await ctx.send(embed=eco_embed)

    #output when shop cat is specified
    elif cat.lower() == 'shop':
      store_embed = discord.Embed(title='Shop Commands List', color=discord.Color.blurple())
  
      store_embed.add_field(name='Bag', value='See what is inside your bag', inline=False)
      store_embed.add_field(name='Shop', value='Look at what we are selling', inline=False)
      store_embed.add_field(name='Buy [item]', value='Buy something from the shop', inline=False)
      store_embed.add_field(name='Sell [item]', value='Sell an item in your bag', inline=False)
  
      await ctx.send(embed=store_embed)

    #output if games cat is specified
    elif cat.lower() == 'games':
      games_embed = discord.Embed(title='Games Commands List', color=discord.Color.blurple())
  
      games_embed.add_field(name='Snake', value='Snake game // aliases: sg', inline=False)
      games_embed.add_field(name='rps [choice]', value='rock paper scissors', inline=False)
      games_embed.add_field(name='tictactoe [bot/user]', value='Tictactoe // aliases: ttt', inline=False)
      games_embed.add_field(name='horsebet [amount] [horse number(1-4)]', value='horsebetting // choose from 4 horses', inline=False)
      games_embed.add_field(name='typingtest', value='Test your typing speed // aliases: tt ; typetest', inline=False)
      games_embed.add_field(name='trivia', value='Test your knowledge & earn coins', inline=False)
      games_embed.add_field(name='blackjack', value='Simplified game of blackjack // aliases: bj', inline=False)
      games_embed.set_footer(text=f"Requested by <@{ctx.author}>", icon_url=ctx.author.avatar)
      await ctx.send(embed=games_embed)

    #output if fish cat is specified
    elif cat.lower() == "fish":
      fish_em = discord.Embed(title="Fish Commands List", color=discord.Color.blurple())
      fish_em.add_field(name="Fish", value="Catch a fish! or trash", inline=False)
      fish_em.add_field(name="Sellfish", value="Sell your fish for coins", inline=False)
      await ctx.send(embed=fish_em)
        
async def setup(client):
  await client.add_cog(HelpCommand(client))
