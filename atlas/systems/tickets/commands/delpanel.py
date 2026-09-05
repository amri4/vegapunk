import discord
from discord.ext import commands

import mycord

db = mycord.PunksDB()

@commands.command(
    name="delpanel",
    help="delete an existing delpanel"
)
async def delpanel(ctx, pan):
    panel = db.fetchone(
        "ticket_panels",
        "panel_id = ?",
        (pan,)
    )
    
    message_id = panel[2]
    message = await channel.fetch_message(message_id)
    await message.delete()
    
    db.delete(
        "ticket_panels",
        "panel_id = ?",
        (pan,)
    )
    await ctx.send("✅️ Panel deleted")

def setup(bot):
    bot.add_command(delpanel)