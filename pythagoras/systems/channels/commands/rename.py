import discord
from discord.ext import commands


@commands.command(
    name="renamechannel",
    help="Rename a channel."
)
async def renamechannel(
    ctx,
    channel: discord.TextChannel = None,
    *,
    name: str = None
):

    if channel is None:
        await ctx.send("❌ Please specify a channel.")
        return

    if not name:
        await ctx.send("❌ Please specify a new name.")
        return

    old_name = channel.name

    await channel.edit(name=name)

    await ctx.send(
        f"✅ Renamed **{old_name}** to **{name}**."
    )


def setup(bot):
    bot.add_command(renamechannel)