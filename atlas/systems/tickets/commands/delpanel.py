import discord
from discord.ext import commands

import mycord

db = mycord.PunksDB()

@commands.command(
    name="delpanel",
    help="delete an existing delpanel"
)
async def delpanel(ctx, pan: int):
    panel = db.fetchone(
        "ticket_panels",
        "panel_id = ?",
        (pan,)
    )
    config = db.fetchone(
        "server_config",
        "guild_id = ?",
        (ctx.guild.id,)
    )
    channel_id = config[4]
    message_id = panel[2]
    channel = ctx.guild.get_channel(channel_id)
    message = channel.fetch_message(message_id)
    await message.delete()
    
    db.delete(
        "ticket_panels",
        "panel_id = ?",
        (pan,)
    )
    await ctx.send("✅️ Panel deleted")

def setup(bot):
    bot.add_command(delpanel)