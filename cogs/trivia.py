import discord
import random
from discord.ext import commands
import json
import asyncio

class TriviaGame(commands.Cog):
    def __init__(self, client):
        self.client = client
        #questions
        self.questions = [
            {
                "question": "What is the capital of France?",
                "options": ["London", "Paris", "Berlin", "Madrid"],
                "correct_option": 1,
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "options": ["Venus", "Mars", "Jupiter", "Neptune"],
                "correct_option": 1,
            },
            {
                "question": "Who painted the Mona Lisa?",
                "options": ["Leonardo da Vinci", "Vincent van Gogh", "Pablo Picasso", "Claude Monet"],
                "correct_option": 0,
            },
            {
              "question": "What is the chemical symbol for water?",
              "options": ["HO", "H2O", "CO2", "NaCl"],
              "correct_option": 1,
            },
            {
              "question": "Who wrote the play 'Romeo and Juliet'?",
              "options": ["Mark Twain", "Jane Austen", "William Shakespeare", "Charles Dickens"],
              "correct_option": 2,
            },
            {
              "question": "What is the largest planet in our solar system?",
              "options": ["Mars", "Saturn", "Jupiter", "Neptune"],
              "correct_option": 2,
            },
            {
              "question": "Which famous scientist developed the theory of general relativity?",
              "options": ["Isaac Newton", "Galileo Galilei", "Marie Curie", "Albert Einstein"],
              "correct_option": 3,
            },
            {
              "question": "In which country would you find the ancient city of Machu Picchu?",
              "options": ["Mexico", "Peru", "Egypt", "Greece"],
              "correct_option": 1,
            },
            {
              "question": "What is the chemical symbol for the element oxygen?",
              "options": ["O", "C", "H", "N"],
              "correct_option": 0,
            },
            {
              "question": "What is the capital city of Japan?",
              "options": ["Beijing", "Tokyo", "Seoul", "Bangkok"],
              "correct_option": 1,
            },
            {
              "question": "Which animal is known as the 'King of the Jungle'?",
              "options": ["Lion", "Tiger", "Elephant", "Gorilla"],
              "correct_option": 0,
            },
            {
              "question": "What is the chemical symbol for gold?",
              "options": ["Go", "Au", "Gd", "Gr"],
              "correct_option": 1,
            },
            {
              "question": "Which novel is authored by Harper Lee?",
              "options": ["To Kill a Mockingbird", "The Catcher in the Rye", "1984", "Pride and Prejudice"],
              "correct_option": 0,
            },
            {
              "question": "In Greek mythology, who is the king of the gods?",
              "options": ["Zeus", "Poseidon", "Hades", "Apollo"],
              "correct_option": 0,
            },
            {
              "question": "Which river is the longest in the world?",
              "options": ["Amazon River", "Nile River", "Yangtze River", "Mississippi River"],
              "correct_option": 1,
            },
            {
              "question": "What is the primary language spoken in Brazil?",
              "options": ["Spanish", "Portuguese", "English", "French"],
              "correct_option": 1
            },
            {
              "question": "What is the capital city of Australia?",
              "options": ["Sydney", "Melbourne", "Canberra", "Brisbane"],
              "correct_option": 2
            }
        ]

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} has loaded.")

    @commands.command(aliases=['trivia'])
    async def triviagame(self, ctx):
        question = random.choice(self.questions)
        question_text = question["question"]
        options = question["options"]

        #randomiing questions
        random.shuffle(options)

        #embedding question
        trivia_embed = discord.Embed(
            title='Trivia Game',
            description=question_text,
            color=discord.Color.blurple()
        )

        #adding options
        for idx, option in enumerate(options):
            trivia_embed.add_field(name=f'{idx + 1}.', value=option, inline=False)

        #outputting question
        await ctx.send(embed=trivia_embed)

        #checking users answer
        def check(msg):
            return msg.author == ctx.author and msg.content.isdigit() and 1 <= int(msg.content) <= len(options)

        try:
            #user has 15 seconds to respond to the trivia question
            response = await self.client.wait_for('message', timeout=15.0, check=check)
            user_choice = int(response.content) - 1
            correct_option = question["correct_option"]
            
            #win condition
            if user_choice == correct_option:
                cor_em = discord.Embed(title='Correct!', description='You earned 5 coins.')
                await ctx.send(embed=cor_em)
                with open("cogs/eco.json", "r") as f:
                  user_eco = json.load(f)

                #check if member has account, if not make one for them
                if str(ctx.author.id) not in user_eco:
                  user_eco[str(ctx.author.id)] = {}
                  user_eco[str(ctx.author.id)]["Wallet"] = 50
                  user_eco[str(ctx.author.id)]["Bank"] = 0

                user_eco[str(ctx.author.id)]["Wallet"] += 5
                with open("cogs/eco.json", "w") as f:
                    json.dump(user_eco, f, indent=4)
            #lose condition
            else:
                wrong_em = discord.Embed(title='Oops!', description="That's incorrect.")
                await ctx.send(embed=wrong_em)

        #time ran out
        except asyncio.TimeoutError:
            await ctx.send("Time's up! The trivia question expired.")

async def setup(client):
    await client.add_cog(TriviaGame(client))
