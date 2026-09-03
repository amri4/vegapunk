import discord
from discord.ext import commands

from ..functions.find_category import find_category


@commands.command(
    name="addchannel",
    help="Create a text channel inside a category."
)
async def addchannel(ctx, *, names: str):

    parts = names.split()

    channel_name = parts[-1]
    category_name = " ".join(parts[:-1])

    category, error = find_category(
        ctx.guild,
        category_name
    )

    if error:
        await ctx.send(error)
        return

    channel = await ctx.guild.create_text_channel(
        name=channel_name,
        category=category
    )

    await ctx.send(
        f"✅ Created {channel.mention} in **{category.name}**."
    )


def setup(bot):
    bot.add_command(addchannel)