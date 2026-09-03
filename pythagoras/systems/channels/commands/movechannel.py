import discord
from discord.ext import commands

from ..functions.find_channel import find_channel
from ..functions.find_category import find_category


@commands.command(
    name="movechannel",
    help="Move a channel above or below another channel or category."
)
async def movechannel(
    ctx,
    channel_input: str = None,
    position: str = None,
    target_input: str = None
):

    if not channel_input:
        await ctx.send("❌ Please specify a channel.")
        return

    if position is None or position.lower() not in ("above", "below"):
        await ctx.send("❌ Position must be `above` or `below`.")
        return

    if not target_input:
        await ctx.send("❌ Please specify the target.")
        return

    channel = find_channel(ctx.guild, channel_input)

    if channel is None:
        await ctx.send("❌ Channel not found.")
        return

    target = find_channel(ctx.guild, target_input)

    if target is None:
        target = find_category(ctx.guild, target_input)

    if target is None:
        await ctx.send("❌ Target channel or category not found.")
        return

    if channel == target:
        await ctx.send("❌ You can't move a channel relative to itself.")
        return

    if position.lower() == "above":
        new_position = target.position + 1
    else:
        new_position = target.position - 1

    await channel.edit(position=new_position)

    await ctx.send(
        f"✅ Moved {channel.mention} "
        f"**{position.lower()}** **{target.name}**."
    )


def setup(bot):
    bot.add_command(movechannel)