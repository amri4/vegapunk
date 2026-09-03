import discord
from discord.ext import commands

from ..functions.find_channel import find_channel


@commands.command(
    name="delchannel",
    help="Delete a channel."
)
async def delchannel(ctx, channel_input: str = None):

    if not channel_input:
        await ctx.send("❌ Please specify a channel.")
        return

    channel = find_channel(ctx.guild, channel_input)

    if channel is None:
        await ctx.send("❌ Channel not found.")
        return

    channel_name = channel.name

    await channel.delete(
        reason=f"Deleted by {ctx.author}"
    )

    await ctx.send(
        f"✅ Deleted **{channel_name}**."
    )


def setup(bot):
    bot.add_command(delchannel)