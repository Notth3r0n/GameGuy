import discord
from discord.ext import commands
import json
import random
import asyncio

EMPTY = "⬜"
PLAYER_X = "❌"
PLAYER_O = "⭕"



class TicTacToe(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} has loaded.")
        
    #display board
    async def display_board(self, ctx, board):
        await ctx.send("".join(board[i] + "\n" if i % 3 == 2 else board[i] for i in range(9)))

    #randomize bots choice
    def get_bot_move(self, board):
        empty_spots = [i for i, spot in enumerate(board) if spot == EMPTY]
        return random.choice(empty_spots)

    @commands.command(aliases=['ttt'])
    async def tictactoe(self, ctx, opponent: str = "bot"):

        #check if choice between bot and user is made
        if opponent.lower() not in ["bot", "user"]:
            await ctx.send("Invalid opponent choice. Please choose 'bot' or 'user'.")
            return
            
        #if choice is user opponent
        if opponent.lower() == "user":
            opp_em = discord.Embed(title='TicTacToe')
            opp_em.add_field(name='Please get opponent to tag himself/herself below', value='▼▼▼')
            await ctx.send(embed=opp_em)
            try:
                opponent = await self.client.wait_for("message", check=lambda m: m.author != ctx.author, timeout=60.0)
                opponent = opponent.author
            except asyncio.TimeoutError:
                await ctx.send("Time's up. The game has ended.")
                return

        # Initialize the game
        board = [EMPTY for _ in range(9)]
        current_player = PLAYER_X
        winner = None

        # Game loop
        while not winner and EMPTY in board:
            await self.display_board(ctx, board)

            if current_player == PLAYER_X:
                def check_valid_move(message):
                    return message.author == ctx.author and message.content.isdigit() and int(message.content) - 1 in [i for i, spot in enumerate(board) if spot == EMPTY]

                try:
                    move = await self.client.wait_for("message", check=check_valid_move, timeout=60.0)
                    move = int(move.content) - 1
                except asyncio.TimeoutError:
                    await ctx.send("Time's up. The game has ended.")
                    return
            # Bot's or user's turn
            else:  
                if opponent == "bot":
                    move = self.get_bot_move(board)
                else:
                    #check if user chose tile inside board
                    def check_valid_move(message):
                        return message.author == opponent and message.content.isdigit() and int(message.content) - 1 in [i for i, spot in enumerate(board) if spot == EMPTY]

                    try:
                        move = await self.client.wait_for("message", check=check_valid_move, timeout=60.0)
                        move = int(move.content) - 1
                    except asyncio.TimeoutError:
                        await ctx.send("Time's up. The game has ended.")
                        return
                        
            if board[move] == EMPTY:
                board[move] = current_player
                winner = self.check_winner(board)
                current_player = PLAYER_O if current_player == PLAYER_X else PLAYER_X
            else:
                if current_player == PLAYER_X:
                    await ctx.send("That spot is already taken. Try again.")

        await self.display_board(ctx, board)

        if winner:
            if winner == PLAYER_X:
                if opponent == "bot":
                    await ctx.send("You win! 5 coins have been credited")
                    with open("cogs/eco.json", "r") as f:
                        user_eco = json.load(f)

                    user_id = str(ctx.author.id)
                    if str(ctx.author.id) not in user_eco:       
                      user_eco[str(ctx.author.id)] = {}
                    
                      user_eco[str(ctx.author.id)]["Wallet"] = 50
                      user_eco[str(ctx.author.id)]["bank"] = 0
                    
                      with open("cogs/eco.json", "w") as f: 
                        json.dump(user_eco, f, indent=4)

                    user_eco[user_id]["Wallet"] += 5

                    with open("cogs/eco.json", "w") as f:
                        json.dump(user_eco, f, indent=4)
                else:
                    await ctx.send("You win! 5 coins have been credited")
                    with open("cogs/eco.json", "r") as f:
                        user_eco = json.load(f)

                    user_id = str(ctx.author.id)
                    if str(ctx.author.id) not in user_eco:       
                      user_eco[str(ctx.author.id)] = {}
                    
                      user_eco[str(ctx.author.id)]["Wallet"] = 50
                      user_eco[str(ctx.author.id)]["bank"] = 0
                    
                      with open("cogs/eco.json", "w") as f: 
                        json.dump(user_eco, f, indent=4)

                    user_eco[user_id]["Wallet"] += 5

                    with open("cogs/eco.json", "w") as f:
                        json.dump(user_eco, f, indent=4)
            elif winner == PLAYER_O:
                if opponent == "bot":
                    await ctx.send("Bot wins!")
                else:
                    await ctx.send(f"{opponent.mention} wins! 5 coins hae been credited")
                    with open("cogs/eco.json", "r") as f:
                        user_eco = json.load(f)

                    user_id = str(opponent.id)
                    if str(opponent.id) not in user_eco:       
                      user_eco[str(opponent.id)] = {}
                    
                      user_eco[str(opponent.id)]["Wallet"] = 50
                      user_eco[str(opponent.id)]["bank"] = 0
                    
                      with open("cogs/eco.json", "w") as f: 
                        json.dump(user_eco, f, indent=4)

                    user_eco[user_id]["Wallet"] += 5

                    with open("cogs/eco.json", "w") as f:
                        json.dump(user_eco, f, indent=4)
            else:
                await ctx.send("It's a tie!")

    def check_winner(self, board):
        lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical
            [0, 4, 8], [2, 4, 6]             # Diagonal
        ]
        for line in lines:
            if board[line[0]] == board[line[1]] == board[line[2]] != EMPTY:
                return board[line[0]]
        return None




async def setup(client):
  await client.add_cog(TicTacToe(client))
