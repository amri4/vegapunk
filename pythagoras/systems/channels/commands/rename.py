import discord
from discord.ext import commands

from ..functions.find_channel import find_channel


@commands.command(
    name="renamechannel",
    help="Rename a channel."
)
async def renamechannel(ctx, channel_input: str = None, *, name: str = None):

    if not channel_input:
        await ctx.send("❌ Please specify a channel.")
        return

    if not name:
        await ctx.send("❌ Please specify a new name.")
        return

    channel = find_channel(ctx.guild, channel_input)

    if channel is None:
        await ctx.send("❌ Channel not found.")
        return

    old_name = channel.name

    await channel.edit(name=name)

    await ctx.send(
        f"✅ Renamed **{old_name}** to **{name}**."
    )


def setup(bot):
    bot.add_command(renamechannel)