import discord
from discord import app_commands


@app_commands.command(
    name="ping",
    description="Check if the bot is online"
)
async def ping(interaction: discord.Interaction):

    embed = discord.Embed(
        title="Pong! 🏓",
        description="The bot is online.",
        color=discord.Color.blurple()
    )

    await interaction.response.send_message(
        embed=embed
    )


def setup(bot):
    bot.tree.add_command(ping)