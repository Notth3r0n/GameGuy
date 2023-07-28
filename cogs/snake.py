import discord
from discord.ext import commands
import json
import random
import asyncio

# Snake constants
EMPTY = "⬜"
FOOD = "🍎"
SNAKE_HEAD = "🟢"
SNAKE_BODY = "🟩"

# Direction constants
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class SnakeGame(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.width = 8
        self.height = 8
        self.snake = [(0, 0)]
        self.direction = RIGHT
        self.generate_food()
        self.running = False
        self.message = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} has loaded.")

    #generate apple on board
    def generate_food(self):
        self.food = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        while self.food in self.snake:
            self.food = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))

    #reset board
    def reset(self):
        self.snake = [(0, 0)]
        self.direction = RIGHT
        self.generate_food()
        self.message = None

    #moving snake
    def move(self):
        head_x, head_y = self.snake[-1]
        if self.direction == UP:
            new_head = (head_x, head_y - 1)
        elif self.direction == RIGHT:
            new_head = (head_x + 1, head_y)
        elif self.direction == DOWN:
            new_head = (head_x, head_y + 1)
        else:
            new_head = (head_x - 1, head_y)

        if new_head in self.snake or new_head[0] < 0 or new_head[0] >= self.width or new_head[1] < 0 or new_head[1] >= self.height:
            return False

        self.snake.append(new_head)
        if new_head == self.food:
            self.generate_food()
            return True
        else:
            self.snake.pop(0)
            return True 

    #get board
    def get_board(self):
        board = [[EMPTY for _ in range(self.width)] for _ in range(self.height)]
        for x, y in self.snake:
            board[y][x] = SNAKE_BODY
        head_x, head_y = self.snake[-1]
        board[head_y][head_x] = SNAKE_HEAD
        food_x, food_y = self.food
        board[food_y][food_x] = FOOD
        return board

    #when reaction is added
    async def on_reaction_add(self, reaction, user):
        if user == self.client.user:
            return

        if self.running and reaction.message.id == self.message.id and user == self.author:
            await self.client.process_commands(reaction.message)

    #edit board to put new position in
    async def update_board(self):
        board = self.get_board()
        board_str = "\n".join("".join(row) for row in board)
        await self.message.edit(content=board_str)

    #show board
    async def display_board(self, ctx):
        board = self.get_board()
        board_str = "\n".join("".join(row) for row in board)
        self.message = await ctx.send(board_str)

    @commands.command(aliases=['sg'])
    async def snake(self, ctx):
        if self.running:
            await ctx.send("A game is already running.")
            return

        self.author = ctx.author

        user_id = str(ctx.author.id)
        with open("cogs/eco.json", "r") as f:
            user_eco = json.load(f)

        #check if member has account, if not make one for them
        if str(ctx.author.id) not in user_eco:
            user_eco[str(ctx.author.id)] = {}

            user_eco[str(ctx.author.id)]["Wallet"] = 50
            user_eco[str(ctx.author.id)]["bank"] = 0

            with open("cogs/eco.json", "w") as f:
                json.dump(user_eco, f, indent=4)

        await ctx.send("Welcome to Snake! Use reactions to control the snake.\n"
                       "React with ⬆️, ➡️, ⬇️, or ⬅️ to move.\n"
                       "Eating an 🍎 will earn you 1 coin.")

        self.running = True
        self.message = None  # Store the board message
        await self.display_board(ctx)  # Display the initial board

      
        while self.running:
            await self.message.add_reaction("⬆️")
            await self.message.add_reaction("➡️")
            await self.message.add_reaction("⬇️")
            await self.message.add_reaction("⬅️")

            def check(reaction, user):
                return (
                    user == ctx.author and
                    str(reaction.emoji) in ["⬆️", "➡️", "⬇️", "⬅️"] and
                    reaction.message.id == self.message.id  # Check if the reaction is on the same message
                )

            try:
                reaction, _ = await self.client.wait_for("reaction_add", check=check, timeout=60.0)
            except asyncio.TimeoutError:
                await ctx.send("Time's up. The game has ended.")
                self.running = False  # Set the running flag to False to exit the loop
                break

            if reaction.emoji == "⬆️":
                self.direction = UP
            elif reaction.emoji == "➡️":
                self.direction = RIGHT
            elif reaction.emoji == "⬇️":
                self.direction = DOWN
            else:
                self.direction = LEFT

            if not self.move():
                await ctx.send("Game Over! Your snake collided with the wall or itself.")
                self.running = False  # Set the running flag to False to exit the loop
                break

            await reaction.remove(ctx.author)  # Remove the user's reaction after processing

            if self.snake[-1] == self.food:
                user_id = str(ctx.author.id)
                with open("cogs/eco.json", "r") as f:
                  user_eco = json.load(f)
                user_eco[user_id]["Wallet"] += 1
                with open("cogs/eco.json", "w") as f:
                    json.dump(user_eco, f, indent=4)
                await self.update_board()
    
            await self.update_board()
            await asyncio.sleep(0.5)

        await asyncio.sleep(1)
        await ctx.send("Game Over! Your snake collided with the wall or itself.")

        self.reset()


async def setup(client):
  await client.add_cog(SnakeGame(client))
