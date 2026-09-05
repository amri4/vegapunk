import asyncio

import discord
from discord.ext import commands

from ..functions.get_message import get_message

import mycord

db = mycord.PunksDB()

@commands.command(
    name="createpanel",
    help="create ticket pannel"
)
async def createpanel(ctx):
   
    await ctx.send("What title do you want for the pannel?")
    message = await get_message(ctx)
    title = message.content

    await ctx.send("Add discription")
    message = await get_message(ctx)
    description = message.content

    embed = discord.Embed(
        title=f"{title}",
        description=f"{description}",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

def setup(bot):
    bot.add_command(createpanel)