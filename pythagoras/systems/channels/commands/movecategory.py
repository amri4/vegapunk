import discord
from discord.ext import commands

from ..functions.find_category import find_category


@commands.command(
    name="movecategory",
    help="Move a category above or below another category."
)
async def movecategory(
    ctx,
    category_input: str = None,
    position: str = None,
    target_input: str = None
):

    if not category_input:
        await ctx.send("❌ Please specify a category.")
        return

    if position is None or position.lower() not in ("above", "below"):
        await ctx.send("❌ Position must be `above` or `below`.")
        return

    if not target_input:
        await ctx.send("❌ Please specify the target category.")
        return

    category = find_category(ctx.guild, category_input)

    if category is None:
        await ctx.send("❌ Category not found.")
        return

    target = find_category(ctx.guild, target_input)

    if target is None:
        await ctx.send("❌ Target category not found.")
        return

    if category == target:
        await ctx.send(
            "❌ You can't move a category relative to itself."
        )
        return

    if position.lower() == "above":
        new_position = target.position + 1
    else:
        new_position = target.position - 1

    await category.edit(position=new_position)

    await ctx.send(
        f"✅ Moved **{category.name}** "
        f"**{position.lower()}** **{target.name}**."
    )


def setup(bot):
    bot.add_command(movecategory)