import discord
from discord import app_commands

from ..functions.berries import get_berries


@app_commands.command(
    name="berries",
    description="Check your berry balance."
)
async def berries(
    interaction: discord.Interaction
):
    amount = get_berries(
        interaction.guild.id,
        interaction.user.id
    )

    await interaction.response.send_message(
        f"🍓 You have **{amount:,} berries**."
    )

def setup(bot):
    bot.tree.add_command(berries)