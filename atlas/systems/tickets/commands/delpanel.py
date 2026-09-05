import discord
from discord.ext import commands

import mycord

db = mycord.PunksDB()

@commands.command(
    name="delpanel",
    help="delete an existing delpanel"
)
async def delpanel(ctx, id):
    await ctx.send("delpanel working")

def setup(bot):
    bot.add_command(delpanel)