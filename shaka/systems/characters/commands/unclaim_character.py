import discord
from discord import app_commands

from ..functions.unclaim_character import unclaim_character
from ..functions.update_panel import update_panel


@app_commands.command(
    name="unclaim_character",
    description="Unclaim your character."
)
async def unclaim(
    interaction: discord.Interaction
):
    if interaction.guild is None:
        return await interaction.response.send_message(
            "❌ This command can only be used in a server."
        )

    character_name = unclaim_character(
        interaction.guild.id,
        interaction.user.id
    )

    if character_name is None:
        return await interaction.response.send_message(
            "❌ You don't have a character claimed."
        )

    await update_panel(
        interaction.client,
        interaction.guild.id
    )

    await interaction.response.send_message(
        f"🏴‍☠️ You unclaimed **{character_name}**."
    )


def setup(bot):
    bot.tree.add_command(unclaim)