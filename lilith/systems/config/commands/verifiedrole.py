import random

import discord
import mycord
from discord import app_commands


db = mycord.DB()

db.create_table(
    "verification_config",
    """
    guild_id INTEGER PRIMARY KEY,
    verified_role_id INTEGER NOT NULL
    """
)


@app_commands.command(
    name="set_verified_role",
    description="Set the role members receive after verification."
)
@app_commands.describe(
    role="The role members will receive when they verify."
)
@app_commands.default_permissions(manage_guild=True)
async def set_verified_role(
    interaction: discord.Interaction,
    role: discord.Role
):
    db.insert_replace(
        "verification_config",
        "guild_id, verified_role_id",
        (
            interaction.guild.id,
            role.id
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
    bot.tree.add_command(set_verified_role)