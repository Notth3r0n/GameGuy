import discord
import random
import time
from discord.ext import commands
import asyncio
import json

class TypingTest(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        time.sleep(0.5)
        print(f"{__name__} has loaded.")
      

    @commands.command(aliases=['tt', 'typetest'])
    async def typingtest(self, ctx):
        test_words = ["apple", "banana", "carrot", "grape", "kiwi",
    "orange", "broccoli", "peach", "potato", "pear",
    "cherry", "lettuce", "watermelon", "tomato", "pineapple",
    "elephant", "computer", "sunflower", "butterfly", "rainbow",
    "chocolate", "waterfall", "fireplace", "television", "telephone",
    "delicious", "mountain", "umbrella", "whisper", "ocean",
    "village", "happiness", "guitar", "piano", "kangaroo",
    "jazz", "elephant", "passion", "mystery", "thunder",
    "discovery", "excellent", "dinosaur", "adventure", "butterfly",
    "nightmare", "champion", "paradise", "umbrella", "friendship",
    "helicopter", "community", "discovery", "fascination", "happiness",
    "universe", "celebration", "reflection", "exploration", "victorious",
    "architecture", "creativity", "waterfall", "thunderstorm", "challenge",
    "fascinating", "captivating", "comfortable", "tremendous", "unbelievable",
    "frightening", "magnificent", "breathtaking", "extraordinary", "fashionable",
    "chandelier", "revolutionary", "inspiration", "satisfaction", "intelligence",
    "comfortable", "relationship", "revolutionary", "responsible", "respectable",
    "information", "interesting", "confidence", "achievement", "competition",
    "appreciation", "incredible", "unforgettable", "imagination", "photograph",
    "communication", "enthusiastic", "announcement", "astronomical", "outstanding"]

        #randomize test word
        test_word = random.choice(test_words)
        #embedding word
        word_em = discord.Embed(title='Typing Test', description='Your word is:', color=discord.Color.blurple())
        word_em.add_field(name='', value=f'**{test_word}**')
        await ctx.reply(embed=word_em)

        try:
            #check if user typed word and if word is the same as test word
            def check(msg):
                return msg.author == ctx.author and msg.content.lower() == test_word

            #start timer
            start_time = time.time()
            #check for message
            await ctx.bot.wait_for('message', timeout=10.0, check=check)
            #once message found, end time
            end_time = time.time()

            #find typing speed
            chars_per_second = len(test_word) / (end_time - start_time)

            average_word_length = 5

            typing_speed_wpm = chars_per_second * 60 / average_word_length
            typing_speed_wpm = round(typing_speed_wpm, 2)

            earned = round(typing_speed_wpm, 0)
            with open("cogs/eco.json", "r") as f:
              user_eco = json.load(f)

            #check if user has account, if not make account
            if str(ctx.author.id) not in user_eco:
              user_eco[str(ctx.author.id)] = {}
              user_eco[str(ctx.author.id)]["Wallet"] = 50
              user_eco[str(ctx.author.id)]["Bank"] = 0

            user_eco[str(ctx.author.id)]["Wallet"] += int(earned)
            with open("cogs/eco.json", "w") as f:
                json.dump(user_eco, f, indent=4)
              
            type_em = discord.Embed(title='Congratulations!', description=f"You typed **{test_word}** correctly in {round(end_time - start_time, 2)} seconds. Your typing speed is {typing_speed_wpm} WPM.")
            type_em.add_field(name='', value=f"You have earned {int(earned)} coins")
            await ctx.reply(embed=type_em)

        except asyncio.TimeoutError:
            late_em = discord.Embed(title='Error!', dscription="Time's up! You didn't type the word in time.")
            await ctx.reply(embed=late_em)

async def setup(client):
  await client.add_cog(TypingTest(client))
