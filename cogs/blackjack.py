import discord
from discord.ext import commands
import random
import json


CARD_VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
BLACKJACK = 21
DEALER_STOP = 17

class BlackjackGame(commands.Cog):
    def __init__(self, client):
        self.client = client

    def draw_card(self):
        return random.choice(list(CARD_VALUES.keys()))

    def calculate_hand_value(self, hand):
        value = sum(CARD_VALUES[card] for card in hand)
        num_aces = hand.count('A')

        while value > BLACKJACK and num_aces > 0:
            value -= 10
            num_aces -= 1

        return value

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} has loaded.")

    #BLACKJACK COMMAND
    @commands.command(aliases=['bj'])
    async def blackjack(self, ctx, amount: int):
        with open("cogs/eco.json", "r") as f:
          user_eco = json.load(f)

        if str(ctx.author.id) not in user_eco:
              user_eco[str(ctx.author.id)] = {}
              user_eco[str(ctx.author.id)]["Wallet"] = 50
              user_eco[str(ctx.author.id)]["Bank"] = 0

        if amount <= 0:
          amount_em = discord.Embed(title="Error!", descripton="Please bet a value greater than 10")
          await ctx.send(embed=amount_em)
        player_hand = [self.draw_card(), self.draw_card()]
        dealer_hand = [self.draw_card(), self.draw_card()]

        def check(m):
            return m.author == ctx.author and m.content.lower() in ('hit', 'stand')

        def format_hand(hand):
            return ' '.join(hand) + f' (Value: {self.calculate_hand_value(hand)})'

        player_em = discord.Embed(title="Blackjack", description=f"Your hand: {format_hand(player_hand)}\n Dealer's hand: {dealer_hand[0]} ?", color=discord.Color.blurple())
        await ctx.send(embed=player_em)

        # Player's turn
        while self.calculate_hand_value(player_hand) < BLACKJACK:
            hitstand_em = discord.Embed(title="",description="Do you want to hit or stand? (Type 'hit' or 'stand')", color=discord.Color.blurple())
            await ctx.send(embed=hitstand_em)
            try:
                response = await self.client.wait_for('message', timeout=30.0, check=check)
                if response.content.lower() == 'hit':
                    player_hand.append(self.draw_card())
                    playerhand_em = discord.Embed(title="Blackjack", description=f'Your hand: {format_hand(player_hand)}', color=discord.Color.blurple())
                    await ctx.send(embed=playerhand_em)
                else:
                    break
            except asyncio.TimeoutError:
                long_em = discord.Embed(title="Error!", description="You took too long to respond. Game over.")
                await ctx.send(embed=long_em)
                return

        player_value = self.calculate_hand_value(player_hand)

        # Dealer's turn
        while self.calculate_hand_value(dealer_hand) < DEALER_STOP:
            dealer_hand.append(self.draw_card())

        dealer_value = self.calculate_hand_value(dealer_hand)

        # Determine the winner
        if player_value > BLACKJACK:
            bust_em = discord.Embed(title="Lost!", description="You bust! Dealer wins.", color=discord.Color.red())
            bust_em.add_field(name="",value=f"You lost {amount} coins")
          
            user_eco[str(ctx.author.id)]["Wallet"] -= amount
            with open("cogs/eco.json", "w") as f:
                json.dump(user_eco, f, indent=4)
              
            await ctx.send(embed=bust_em)
          
        elif dealer_value > BLACKJACK:
            dealer_bust_em = discord.Embed(title="Won!", description="Dealer busts! You win.", color=discord.Color.green())
            dealer_bust_em.add_field(name="",value=f"You won {amount} coins")

            user_eco[str(ctx.author.id)]["Wallet"] += amount
            with open("cogs/eco.json", "w") as f:
                json.dump(user_eco, f, indent=4)
          
            await ctx.send(embed=dealer_bust_em)
          
        elif player_value == dealer_value:
            tie_em = discord.Embed(title="Blackjack", description="It's a tie!", color=discord.Color.blurple())
            
            await ctx.send(embed=tie_em)
          
        elif player_value > dealer_value:
            win_em = discord.Embed(title="Blackjack", description="You win!", color=discord.Color.green())
            win_em.add_field(name="",value=f"You won {amount} coins")

            user_eco[str(ctx.author.id)]["Wallet"] += amount
            with open("cogs/eco.json", "w") as f:
                json.dump(user_eco, f, indent=4)
          
            await ctx.send(embed=win_em)
          
        else: 
            lose_em = discord.Embed(title="Lost", description="Dealer wins!", color=discord.Color.red())
            lose_em.add_field(name="",value=f"You lost {amount} coins")

            user_eco[str(ctx.author.id)]["Wallet"] -= amount
            with open("cogs/eco.json", "w") as f:
                json.dump(user_eco, f, indent=4)
          
            await ctx.send(embed=lose_em)
          
        player_hand_em = discord.Embed(title="", description=f"Your hand: {format_hand(player_hand)}\n Dealer's hand: {format_hand(dealer_hand)}", color=discord.Color.blurple())
        await ctx.send(embed=player_hand_em)

async def setup(client):
    await client.add_cog(BlackjackGame(client))
