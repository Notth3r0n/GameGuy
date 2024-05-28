import discord
from discord.ext import commands
import random
import json
import time


class mod(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        time.sleep(0.5)
        print(f"{__name__} has loaded.")

    #warn command
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        with open('warn.json', 'r') as f:
            warns = json.load(f)

        if str(member.id) in warns:
            warns[str(member.id)]['warns'] += 1
            warns[str(member.id)]['reasons'][str(warns[str(
                member.id)]['warns'])] = reason

        else:
            warns[str(member.id)] = {'warns': 1, 'reasons': {'1': reason}}

        with open('warn.json', 'w') as f:
            json.dump(warns, f, indent=4)

        warn_embed = discord.Embed(
            title='Warned',
            description=
            f"{member} has been warned for **{reason}**\n\nTotal Warnings: **{warns[str(member.id)]['warns']}**"
        )
        await ctx.reply(embed=warn_embed)

    #warnings command
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warnings(self, ctx, member: discord.Member):
        with open('warn.json', 'r') as f:
            warns = json.load(f)

        warn_embed = discord.Embed(
            title='Warn Check',
            description=
            f"{member} has a total of {warns[str(member.id)]['warns']} warnings.\n\n"
        )

        for key, value in warns[str(member.id)]['reasons'].items():
            warn_embed.add_field(name=f"Warning {key}", value=value)

        await ctx.reply(embed=warn_embed)

    #kick command
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        kick_em = discord.Embed(
            title='Kicked',
            description=f'{member} has been kicked for {reason}')
        await ctx.reply(Embed=kick_em)

    #ban command
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        ban_em = discord.Embed(
            title='Banned',
            description=f'{member} has been banned for {reason}')
        with open('banned.json', 'r') as f:
            banned = json.load(f)
        banned[str(member.id)] = {'username': member.name, 'reason': reason}
        with open('banned.json', 'w') as f:
            json.dump(banned, f, indent=4)
        await ctx.reply(embed=ban_em)

    #unban command
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.Member, *, reason=None):
        with open('banned.json', 'r') as f:
            banned = json.load(f)
        if str(member.id) in banned:
            del banned[str(member.id)]
            with open('banned.json', 'w') as f:
                json.dump(banned, f, indent=4)
            unb_em = discord.Embed(
                title='Unbanned',
                description=f'{member} has been unbanned for {reason}')
            await ctx.reply(Embed=unb_em)
        else:
            er_em = discord.Embed(title='Error',
                                  description=f'{member} is not banned')
            await ctx.reply(Embed=er_em)


async def setup(client):
    await client.add_cog(mod(client))