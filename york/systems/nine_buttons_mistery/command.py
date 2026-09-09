import discord
from discord import app_commands

from .view import MysteryView


@app_commands.command(
    name="mysterybox",
    description="Open a mystery box!"
)
async def mysterybox(interaction: discord.Interaction):
    view = MysteryView(interaction.user.id)

    await interaction.response.send_message(
        embed=view.game_embed(),
        view=view
    )


def setup(bot):
    bot.tree.add_command(mysterybox)