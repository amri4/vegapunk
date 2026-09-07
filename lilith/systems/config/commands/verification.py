import random

import discord
from discord import app_commands

from .panel import send_verification_panel
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

    if status.value == "on":

        if config[3] == 1:
            await interaction.response.send_message(
                "Tch. Verification is already enabled."
            )
            return

        channel = await interaction.guild.create_text_channel(
            "verification"
        )

        db.update(
            "verification_config",
            "verification_channel_id = ?, enabled = 1",
            "guild_id = ?",
            (
                channel.id,
                interaction.guild.id
            )
        )

        await send_verification_panel(channel)

        responses = [
            f"🛡️ Verification is now online. {channel.mention} has been created.",
            f"Tch. The verification gate is active in {channel.mention}.",
            f"🔐 Verification enabled. I've created {channel.mention}."
        ]

    else:

        if config[3] == 0:
            await interaction.response.send_message(
                "Tch. Verification is already disabled."
            )
            return

        channel = None

        if config[2]:
            channel = interaction.guild.get_channel(
                config[2]
            )

        if channel:
            try:
                await channel.delete(
                    reason=f"Verification disabled by {interaction.user}"
                )
            except discord.HTTPException:
                pass

        db.update(
            "verification_config",
            "verification_channel_id = NULL, enabled = 0",
            "guild_id = ?",
            (interaction.guild.id,)
        )

        responses = [
            "🔓 Verification is now disabled. The verification channel is gone.",
            "Tch. The verification gate is down. Channel removed.",
            "Verification disabled. I've cleaned up the verification channel."
        ]

    await interaction.response.send_message(
        random.choice(responses)
    )


def setup(bot):
    bot.tree.add_command(verification)