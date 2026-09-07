import random

import discord
from discord import app_commands

from .setup import db


@app_commands.command(
    name="verification",
    description="Turn the server verification system on or off."
)
@app_commands.describe(
    status="Turn verification on or off."
)
@app_commands.choices(
    status=[
        app_commands.Choice(name="On", value="on"),
        app_commands.Choice(name="Off", value="off")
    ]
)
@app_commands.default_permissions(manage_guild=True)
async def verification(
    interaction: discord.Interaction,
    status: app_commands.Choice[str]
):
    config = db.fetchone(
        "verification_config",
        "guild_id = ?",
        (interaction.guild.id,)
    )

    if config is None or config[1] is None:
        responses = [
            "Tch. You haven't configured a verification role yet.",
            "I need a verification role before I can activate this.",
            "Set the verified role first. Then I'll handle the rest."
        ]

        await interaction.response.send_message(
            random.choice(responses)
        )
        return

    db.update(
        "verification_config",
        "enabled = ?",
        "guild_id = ?",
        (
            1 if status.value == "on" else 0,
            interaction.guild.id
        )
    )

    if status.value == "on":
        responses = [
            "🛡️ Verification is now online.",
            "Tch. The verification gate is active.",
            "🔐 Verification enabled. Keep the intruders out."
        ]
    else:
        responses = [
            "🔓 Verification is now disabled.",
            "Tch. The verification gate is down.",
            "Verification has been switched off."
        ]

    await interaction.response.send_message(
        random.choice(responses)
    )


def setup(bot):
    bot.tree.add_command(verification)