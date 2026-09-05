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

    #CHECK IF EMBED CHANNEL IS CONFIGURED
    config = db.fetchone(
        "server_config",
        "guild_id = ?",
        (ctx.guild.id,)
    )
    channel_id = config[4]
    channel = ctx.guild.get_channel(channel_id)
    if channel_id is None:
        await ctx.send("There is no ticket pannel channel configured, go ask pythagoras")
        return

    #TITLE
    await ctx.send("What title do you want for the pannel?")
    message = await get_message(ctx)
    title = message.content

    #DESCRIPTION
    await ctx.send("Add discription")
    message = await get_message(ctx)
    description = message.content

    #IMAGE
    await ctx.send("Add image or type `skip` to skip")
    message = await get_message(ctx)
    if message.content.lower() == "skip":
        image_url = None
    else:
        image_url = message.attachments[0].url

    #THUMBNAIL
    await ctx.send("Add thumbnail or type `skip` to skip")
    message = await get_message(ctx)
    if message.content.lower() == "skip":
        thumbnail_url = None
    else:
        thumbnail_url = message.attachments[0].url

    #EMBED
    embed = discord.Embed(
        title=f"{title}",
        description=f"{description}",
        color=discord.Color.blue()
    )
    embed.set_image(url=image_url)
    embed.set_thumbnail(url=thumbnail_url)
    
    message = await channel.send(embed=embed)

    print("BEFORE INSERT")
    db.insert(
        "ticket_panels",
        "guild_id, message_id, title, description, image_url, thumbnail_url",
        (ctx.guild.id, message.id, title, description, image_url, thumbnail_url)
    )
    print("AFTER INSERT")
    panel = db.fetchone(
        "ticket_panels",
        "message_id = ?",
        (message.id,)
    )
    print("FETCHED", panel)
    panel_id = panel[0]
    print("PANEL_ID:", panel_id)

    embed.set_footer(text=f"PANEL_ID: {panel_id}")
    await message.edit(embed=embed)
    print("EDITED")
    
    await ctx.send("✅️ Pannel created.")

def setup(bot):
    bot.add_command(createpanel)