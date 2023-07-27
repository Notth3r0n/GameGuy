import discord
from discord.ext import commands
import json

elec_shop = [
    {"name": "Watch", "price": 600, "description": "Your own mobile device"},
    {"name": "Phone", "price": 900, "description": "Tell time from your wrist"},
    {"name": "PC", "price": 1250, "description": "Computer"},
    {"name": "Laptop", "price": 2900, "description": "Handheld computer"}
]
weapons_shop = [
    {"name": "Knife", "price": 350, "description": "knife"},
    {"name": "Sword", "price": 500, "description": "Sword"},
    {"name": "Pistol", "price": 700, "description": "No details needed:)"},
    {"name": "AK-47", "price": 900, "description": "No details needed:)"},
    {"name": "Shotgun", "price": 1200, "description": "No details needed:)"},
    {"name": "Rocket Launcher", "price": 1400, "description": "BOOM"}
]
fish_shop = [
    {"name": "Common fishing rod", "price": 300, "description": "Most mid fishing rod"},
    {"name": "Uncommon fishing rod", "price": 500, "description": "Not so mid fishing rod"},
    {"name": "Rare fishing rod", "price": 700, "description": "Mid but better fishing rod"},
    {"name": "Epic fishing rod", "price": 900, "description": "Just a better fishing rod"},
    {"name": "Legendary fishing rod", "price": 1100, "description": "Even better fishing rod"},
    {"name": "Mythic fishing rod", "price": 1300, "description": "Best fishing rod"}
]





class Store(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} has loaded.")

    # Shop COMMAND
    @commands.command()
    async def shop(self, ctx):
        elec_em = discord.Embed(title='Electronics Shop', colour=discord.Color.blurple())
        weapons_em = discord.Embed(title='Weapons Shop', colour=discord.Color.blurple())
        fish_em = discord.Embed(title='Fish Shop', description="Each tier reduces chances of trash caught", colour=discord.Color.blurple())

        
        for item in elec_shop:
            name = item["name"]
            price = item["price"]
            desc = item["description"]
            elec_em.add_field(name=name, value=f'{price} coins | {desc}')

        for item in weapons_shop:
            name = item["name"]
            price = item["price"]
            desc = item["description"]
            weapons_em.add_field(name=name, value=f'{price} coins | {desc}')

        for item in fish_shop:
            name = item["name"]
            price = item["price"]
            desc = item["description"]
            fish_em.add_field(name=name, value=f'{price} coins | {desc}')
        fish_em.set_footer(text="Once fishing rod upgraded, old fishing rod is removed.")
          
        await ctx.send(embed=elec_em)
        await ctx.send(embed=weapons_em)
        await ctx.send(embed=fish_em)
      
    #Buy COMMAND
    @commands.command()
    async def buy(self, ctx, *, item):
        item = item.lower()
        for i in elec_shop:
            name = i["name"].lower()
            price = i["price"]
        for i in weapons_shop:
            name1 = i["name"].lower()
            price1 = i["price"]
        for i in fish_shop:
            name2 = i["name"].lower()
            price2 = i["price"]

            if name == item:
                with open("cogs/inven.json", "r") as f:
                    user_inven = json.load(f)

                with open("cogs/eco.json", "r") as f:
                    user_eco = json.load(f)

                user_id = str(ctx.author.id)
                if user_id not in user_inven:
                    user_inven[user_id] = {}
                    user_inven[user_id]["Bag"] = []
                    user_inven[str(ctx.author.id)]["Fish Bag"] = []
                    with open("cogs/inven.json", "w") as f:
                        json.dump(user_inven, f, indent=4)

                if "Wallet" not in user_eco[user_id]:
                    user_eco[user_id]["Wallet"] = 0
                if "Bank" not in user_eco[user_id]:
                    user_eco[user_id]["Bank"] = 0

                if user_eco[user_id]["Wallet"] >= price:
                    user_inven[user_id]["Bag"].append(name)
                    user_eco[user_id]["Wallet"] -= price

                    item_em = discord.Embed(title=f'You have purchased a {name}')
                    item_em.add_field(name=f'{price} coins have been deducted from your wallet', value='lol')
                    await ctx.send(embed=item_em)

                    with open("cogs/inven.json", "w") as f:
                        json.dump(user_inven, f, indent=4)
                    with open("cogs/eco.json", "w") as f:
                        json.dump(user_eco, f, indent=4)

                elif user_eco[user_id]["Bank"] >= price:
                    user_inven[user_id]["Bag"].append(name)
                    user_eco[user_id]["Bank"] -= price

                    item_em = discord.Embed(title=f'You have purchased a {name}')
                    item_em.add_field(name=f'{price} coins have been deducted from your bank', value='lol')
                    await ctx.send(embed=item_em)

                    with open("cogs/inven.json", "w") as f:
                        json.dump(user_inven, f, indent=4)
                    with open("cogs/eco.json", "w") as f:
                        json.dump(user_eco, f, indent=4)

                else:
                    broke_em = discord.Embed(title='Error!')
                    broke_em.add_field(name='You do not have enough coins', value="You're broke")
                    await ctx.send(embed=broke_em)
                return

            if name1 == item:
                with open("cogs/inven.json", "r") as f:
                    user_inven = json.load(f)

                with open("cogs/eco.json", "r") as f:
                    user_eco = json.load(f)

                user_id = str(ctx.author.id)
                if user_id not in user_inven:
                    user_inven[user_id] = {}
                    user_inven[user_id]["Bag"] = []
                    user_inven[str(ctx.author.id)]["Fish Bag"] = []
                    with open("cogs/inven.json", "w") as f:
                        json.dump(user_inven, f, indent=4)

                if "Wallet" not in user_eco[user_id]:
                    user_eco[user_id]["Wallet"] = 0
                if "Bank" not in user_eco[user_id]:
                    user_eco[user_id]["Bank"] = 0

                if user_eco[user_id]["Wallet"] >= price1:
                    user_inven[user_id]["Bag"].append(name1)
                    user_eco[user_id]["Wallet"] -= price1

                    item_em = discord.Embed(title=f'You have purchased a {name1}')
                    item_em.add_field(name=f'{price1} coins have been deducted from your wallet', value='lol')
                    await ctx.send(embed=item_em)

                    with open("cogs/inven.json", "w") as f:
                        json.dump(user_inven, f, indent=4)
                    with open("cogs/eco.json", "w") as f:
                        json.dump(user_eco, f, indent=4)

                elif user_eco[user_id]["Bank"] >= price1:
                    user_inven[user_id]["Bag"].append(name1)
                    user_eco[user_id]["Bank"] -= price1

                    item_em = discord.Embed(title=f'You have purchased a {name1}')
                    item_em.add_field(name=f'{price1} coins have been deducted from your bank', value='lol')
                    await ctx.send(embed=item_em)

                    with open("cogs/inven.json", "w") as f:
                        json.dump(user_inven, f, indent=4)
                    with open("cogs/eco.json", "w") as f:
                        json.dump(user_eco, f, indent=4)

                else:
                    broke_em = discord.Embed(title='Error!')
                    broke_em.add_field(name='You do not have enough coins', value="You're broke")
                    await ctx.send(embed=broke_em)
                return

            if name2 == item:
                with open("cogs/inven.json", "r") as f:
                    user_inven = json.load(f)

                with open("cogs/eco.json", "r") as f:
                    user_eco = json.load(f)

                user_id = str(ctx.author.id)
                if user_id not in user_inven:
                    user_inven[user_id] = {}
                    user_inven[user_id]["Bag"] = []
                    user_inven[str(ctx.author.id)]["Fish Bag"] = []
                    with open("cogs/inven.json", "w") as f:
                        json.dump(user_inven, f, indent=4)

                if "Wallet" not in user_eco[user_id]:
                    user_eco[user_id]["Wallet"] = 0
                if "Bank" not in user_eco[user_id]:
                    user_eco[user_id]["Bank"] = 0

                if user_eco[user_id]["Wallet"] >= price2:
                    bag = user_inven[user_id]["Bag"]
                    if "common fishing rod" in bag:
                      bag.remove("common fishing rod")
                    elif "uncommon fishing rod" in bag:
                      bag.remove("uncommon fishing rod")
                    elif "rare fishing rod" in bag:
                      bag.remove("rare fishing rod")
                    elif "epic fishing rod" in bag:
                      bag.remove("epic fishing rod")
                    elif "legendary fishing rod" in bag:
                      bag.remove("legendary fishing rod")
                      
                    user_inven[user_id]["Bag"].append(name2)
                    user_eco[user_id]["Wallet"] -= price2

                    item_em = discord.Embed(title=f'You have purchased a {name2}')
                    item_em.add_field(name=f'{price2} coins have been deducted from your wallet', value='lol')
                    await ctx.send(embed=item_em)

                    with open("cogs/inven.json", "w") as f:
                        json.dump(user_inven, f, indent=4)
                    with open("cogs/eco.json", "w") as f:
                        json.dump(user_eco, f, indent=4)

                elif user_eco[user_id]["Bank"] >= price2:
                    bag = user_inven[user_id]["Bag"]
                    if "common fishing rod" in bag:
                      bag.remove("common fishing rod")
                    elif "uncommon fishing rod" in bag:
                      bag.remove("uncommon fishing rod")
                    elif "rare fishing rod" in bag:
                      bag.remove("rare fishing rod")
                    elif "epic fishing rod" in bag:
                      bag.remove("epic fishing rod")
                    elif "legendary fishing rod" in bag:
                      bag.remove("legendary fishing rod")

                    user_inven[user_id]["Bag"].append(name2)
                    user_eco[user_id]["Bank"] -= price2

                    item_em = discord.Embed(title=f'You have purchased a {name2}')
                    item_em.add_field(name=f'{price2} coins have been deducted from your bank', value='lol')
                    await ctx.send(embed=item_em)

                    with open("cogs/inven.json", "w") as f:
                        json.dump(user_inven, f, indent=4)
                    with open("cogs/eco.json", "w") as f:
                        json.dump(user_eco, f, indent=4)

                else:
                    broke_em = discord.Embed(title='Error!')
                    broke_em.add_field(name='You do not have enough coins', value="You're broke")
                    await ctx.send(embed=broke_em)

                

                

                return

        # If the item was not found in the shop
        not_found_em = discord.Embed(title='Error!')
        not_found_em.add_field(name='Item not found in the shop', value='Please enter a valid item.')
        await ctx.send(embed=not_found_em)

    # Inven COMMAND
    @commands.command(aliases=["inventory"])
    async def bag(self, ctx, member: discord.Member = None):
        with open("cogs/inven.json", "r") as f:
            user_inven = json.load(f)

        if member is None:
            member = ctx.author
        elif member is not None:
            member = member

        if str(member.id) not in user_inven:
            user_inven[str(member.id)] = {}
            user_inven[str(member.id)]["Bag"] = []
            user_inven[str(ctx.author.id)]["Fish Bag"] = []
            with open("cogs/inven.json", "w") as f:
                json.dump(user_inven, f, indent=4)

        fish_bag = user_inven[str(ctx.author.id)]["Fish Bag"]
        fish_names = [fish["name"] for fish in fish_bag]
        fish_list = ', '.join(fish_names)
        bag = user_inven[str(ctx.author.id)]["Bag"]
        bag_list = ', '.join(bag)

        bag_embed = discord.Embed(title=f"{member.name}'s items", color=discord.Color.blue())
        bag_embed.add_field(name="Bag:", value=f"{bag_list}", inline=False)
        bag_embed.add_field(name="Fish Bag:", value=f"{fish_list}", inline=False)
        await ctx.send(embed=bag_embed)

    # Sell COMMAND
    @commands.command()
    async def sell(self, ctx, *, item):
        with open("cogs/inven.json", "r") as f:
            user_inven = json.load(f)
    
        with open("cogs/eco.json", "r") as f:
            user_eco = json.load(f)

        user_id = str(ctx.author.id)
        bag = user_inven[user_id]["Bag"]
      
        if item not in bag:
            dont_em = discord.Embed(title='Error!', description="You don't have that item in your bag.")
            await ctx.send(embed=dont_em)
            return
          
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ['yes', 'no']
                
        check_em = discord.Embed(title="Sell", description="You will only be refunded 80% of the item's value. Do you want to continue? (Type 'yes' or 'no')")
        await ctx.send(embed=check_em)
      
        try:
            response = await self.client.wait_for('message', timeout=15.0, check=check)
        except asyncio.TimeoutError:
            timeout_em = discord.Embed(title="Timeout", description="You took too long to respond. The command has been cancelled.")
            await ctx.send(embed=timeout_em)
            return

        if response.content.lower() == 'yes':
            item = item.lower()
            
            # Assuming elec_shop, weapons_shop, and fish_shop are defined elsewhere
            shop_data = elec_shop + weapons_shop + fish_shop
            item_data = next((i for i in shop_data if i["name"].lower() == item), None)
    
            if not item_data:
                await ctx.send("Item not found in the shop data.")
                return
    
            item_price = item_data["price"]
            item_price = item_price * 0.8
    
            bag.remove(item)
            user_eco[user_id]["Wallet"] += int(item_price)
    
            with open("cogs/inven.json", "w") as f:
                json.dump(user_inven, f, indent=4)
            with open("cogs/eco.json", "w") as f:
                json.dump(user_eco, f, indent=4)
    
            sell_em = discord.Embed(title=f"You sold a {item}", description=f"You earned {int(item_price)} coins!")
            await ctx.send(embed=sell_em)
        else:
            cancel_em = discord.Embed(title="Cancel", description="You have cancelled the command.")
            await ctx.send(embed=cancel_em)



async def setup(client):
    await client.add_cog(Store(client))
