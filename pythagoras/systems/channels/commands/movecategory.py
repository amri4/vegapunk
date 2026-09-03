import discord
from discord.ext import commands

from ..functions.find_category import find_category


@commands.command(
    name="movecategory",
    help="Move a category above or below another category.",
    usage="<category> <above/below> <target>"
)
async def movecategory(ctx, *, arguments: str):

    parts = arguments.split()

    if len(parts) < 3:
        await ctx.send(
            "❌ Usage: "
            "`Pythagoras movecategory <category> "
            "<above/below> <target>`"
        )
        return

    # FIND SOURCE CATEGORY

    source = None
    source_end = None

    for i in range(1, len(parts)):

        possible = " ".join(parts[:i])

        found = find_category(
            ctx.guild,
            possible
        )

        if found:
            source = found
            source_end = i
            break

    if not source:
        await ctx.send(
            "❌ I couldn't find the category "
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

    # FIND TARGET CATEGORY

    target_text = " ".join(
        parts[source_end + 1:]
    )

    target = find_category(
        ctx.guild,
        target_text
    )

    if not target:
        await ctx.send(
            "❌ I couldn't find the "
            "target category."
        )
        return

    if source.id == target.id:
        await ctx.send(
            "❌ You can't move a category "
            "relative to itself."
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
        f"📁 Moved category "
        f"**{source.name}** "
        f"**{direction}** "
        f"**{target.name}**."
    )


def setup(bot):
    bot.add_command(movecategory)