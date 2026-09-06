import discord
from discord.ext import commands


@commands.command(
    name="help",
    description="Show the bot's commands"
)
async def help_command(ctx):

    embed = discord.Embed(
        title=f"{ctx.bot.bot_name} Help",
        description="Here are my commands:",
        color=discord.Color.blurple()
    )

    for command in ctx.bot.commands:

        if command.name == "help":
            continue

        embed.add_field(
            name=f"Atlas {command.name}",
            value=command.help or "No description.",
            inline=False
        )

    await ctx.send(embed=embed)


def setup(bot):

    bot.add_command(help_command)