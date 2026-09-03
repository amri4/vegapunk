import discord
from discord.ext import commands


@commands.command(
    name="addchannel",
    help="Create a text channel inside a category."
)
async def addchannel(
    ctx,
    category: discord.CategoryChannel,
    *,
    channel: str
):
    new_channel = await ctx.guild.create_text_channel(
        name=channel,
        category=category
    )

    await ctx.send(
        f"Created {new_channel.mention} in **{category.name}**."
    )


def setup(bot):
    bot.add_command(addchannel)