import asyncio

import discord
from discord.ext import commands

import mycord

db = mycord.PunksDB()

@commands.command()
async def createpanel(ctx):
    await ctx.send("Command worked")

def setup(bot):
    bot.add_command(createpanel)