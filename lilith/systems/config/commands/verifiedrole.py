import random

import discord
from discord import app_commands

from .setup import db


@app_commands.command(
    name="set_verified_role",
    description="Set the role members receive after verification."
)
@app_commands.describe(
    role="The role members will receive when they verify."
)
@app_commands.default_permissions(
    manage_guild=True
)
async def set_verified_role(
    interaction: discord.Interaction,
    role: discord.Role
):
    db.insert_replace(
        "verification_config",
        "guild_id, verified_role_id, verification_channel_id, enabled",
        (
            interaction.guild.id,
            role.id,
            None,
            0
        )
    )

    responses = [
        f"🛡️ {role.mention} is now the verification role.",
        f"Tch. Verification will now use {role.mention}.",
        f"Done. Members who verify will receive {role.mention}.",
        f"🔐 Verification role configured as {role.mention}."
    ]

    await interaction.response.send_message(
        random.choice(responses)
    )


def setup(bot):
    bot.tree.add_command(
        set_verified_role
    )