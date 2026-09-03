import discord
from discord.ext import commands


@commands.command(
    name="addcategory",
    help="Create a new server category."
)
async def addcategory(ctx, *, name: str):

    name = name.strip()

    if not name:
        await ctx.send(
            "❌ Please provide a category name."
        )
        return

    category = await ctx.guild.create_category(
        name=name,
        reason=f"Created by {ctx.author}"
    )

    await ctx.send(
        f"✅ Created category **{category.name}**."
    )


def setup(bot):
    bot.add_command(addcategory)