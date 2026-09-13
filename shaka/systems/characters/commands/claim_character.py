import discord
from discord import app_commands

from ..data.characters import CHARACTERS
from ..functions.claim_character import claim_character
from ..functions.update_panel import update_panel


def title_name(name):
    parts = name.split(".")
    result = []

    for part in parts:
        if part == "D":
            result.append("D.")
        else:
            result.append(part.title())

    return " ".join(result).strip()


async def character_autocomplete(
    interaction: discord.Interaction,
    current: str
):
    current = current.lower()

    choices = []

    for character in CHARACTERS:
        name = title_name(character)

        if current in name.lower():
            choices.append(
                app_commands.Choice(
                    name=name[:100],
                    value=name
                )
            )

        if len(choices) >= 25:
            break

    return choices


@app_commands.command(
    name="claim_character",
    description="Claim a character."
)
@app_commands.describe(
    character="The character you want to claim."
)
@app_commands.autocomplete(character=character_autocomplete)
async def claim(
    interaction: discord.Interaction,
    character: str
):
    if interaction.guild is None:
        return await interaction.response.send_message(
            "❌ This command can only be used in a server."
        )

    success = claim_character(
        interaction.guild.id,
        character,
        interaction.user.id
    )

    if not success:
        return await interaction.response.send_message(
            f"❌ **{character}** is already claimed."
        )

    await update_panel(
        interaction.client,
        interaction.guild.id
    )

    await interaction.response.send_message(
        f"🏴‍☠️ You claimed **{character}**!"
    )


def setup(bot):
    bot.tree.add_command(claim)