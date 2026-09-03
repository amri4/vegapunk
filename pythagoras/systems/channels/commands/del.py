import discord
from discord.ext import commands


@commands.command(
    name="delchannel",
    help="Delete a channel."
)
async def delchannel(ctx, channel: discord.TextChannel = None):

    if channel is None:
        await ctx.send("❌ Please specify a channel.")
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