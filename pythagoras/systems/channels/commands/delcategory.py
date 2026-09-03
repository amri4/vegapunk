import discord
from discord.ext import commands

from ..functions.find_category import find_category


@commands.command(
    name="delcategory",
    help="Delete a server category."
)
async def delcategory(ctx, *, name: str):

    category = find_category(
        ctx.guild,
        name
    )

    if category is None:
        await ctx.send(
            "❌ I couldn't find that category."
        )
        return

    category_name = category.name

    await category.delete(
        reason=f"Deleted by {ctx.author}"
    )

    await ctx.send(
        f"🗑️ Deleted category **{category_name}**."
    )


def setup(bot):
    bot.add_command(delcategory)