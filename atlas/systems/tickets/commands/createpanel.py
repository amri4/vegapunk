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

    await ctx.send("Add image or type `skip` to skip")
    message = await get_message(ctx)
    if message.content.lower() == "skip":
        image_url = None
    else:
        image_url = message.attachments[0].url

    embed = discord.Embed(
        title=f"{title}",
        description=f"{description}",
        color=discord.Color.blue()
    )
    embed.set_image(url=image_url)
    await ctx.send(embed=embed)

def setup(bot):
    bot.add_command(createpanel)