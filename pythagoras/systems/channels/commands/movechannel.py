import discord
from discord.ext import commands

from ..functions.find_channel import find_channel


@commands.command(
    name="movechannel",
    help="Move a channel above or below another channel.",
    usage="<channel> <above/below> <target>"
)
async def movechannel(ctx, *, arguments: str):

    parts = arguments.split()

    if len(parts) < 3:
        await ctx.send(
            "❌ Usage: "
            "`Pythagoras movechannel <channel> "
            "<above/below> <target>`"
        )
        return

    # FIND SOURCE CHANNEL

    source = None
    source_end = None

    for i in range(1, len(parts)):

        possible = " ".join(parts[:i])

        found = find_channel(
            ctx.guild,
            possible
        )

        if found:
            source = found
            source_end = i
            break

    if not source:
        await ctx.send(
            "❌ I couldn't find the channel "
            "you want to move."
        )
        return

    # DIRECTION

    if source_end >= len(parts):
        await ctx.send(
            "❌ Please specify `above` or `below`."
        )
        return

    direction = parts[source_end].lower()

    if direction not in ("above", "below"):
        await ctx.send(
            "❌ Direction must be `above` or `below`."
        )
        return

    # FIND TARGET

    target_text = " ".join(
        parts[source_end + 1:]
    )

    target = find_channel(
        ctx.guild,
        target_text
    )

    if not target:
        await ctx.send(
            "❌ I couldn't find the target channel."
        )
        return

    if source.id == target.id:
        await ctx.send(
            "❌ You can't move a channel "
            "relative to itself."
        )
        return

    # SAME CATEGORY

    if source.category_id != target.category_id:
        await ctx.send(
            "❌ Both channels must be "
            "in the same category."
        )
        return

    # MOVE

    target_position = target.position

    if direction == "above":
        new_position = target_position
    else:
        new_position = target_position + 1

    await source.edit(
        position=new_position,
        reason=f"Moved by {ctx.author}"
    )

    await ctx.send(
        f"📁 Moved {source.mention} "
        f"**{direction}** {target.mention}."
    )


def setup(bot):
    bot.add_command(movechannel)