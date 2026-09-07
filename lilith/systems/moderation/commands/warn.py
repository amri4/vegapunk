import random

import discord
import mycord
from discord import app_commands


db = mycord.DB()

db.create_table(
    "warnings",
    """
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guild_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    moderator_id INTEGER NOT NULL,
    reason TEXT NOT NULL,
    created_at TEXT NOT NULL
    """
)


@app_commands.command(
    name="warn",
    description="Warn a member."
)
@app_commands.describe(
    member="The member you want to warn.",
    reason="Why the member is being warned."
)
@app_commands.default_permissions(moderate_members=True)
async def warn(
    interaction: discord.Interaction,
    member: discord.Member,
    reason: str = "No reason provided."
):
    if member.id == interaction.user.id:
        responses = [
            "You want to warn yourself? What exactly am I supposed to write?",
            "Tch. I'm not giving you a warning just because you asked.",
            "If you know you've done something wrong, fix it."
        ]

        await interaction.response.send_message(random.choice(responses))
        return

    if member.id == interaction.guild.owner_id:
        responses = [
            "I'm not warning the owner. Find someone else to handle it.",
            "Tch. You expect me to warn the owner?",
            "That's above my authority."
        ]

        await interaction.response.send_message(random.choice(responses))
        return

    if member.top_role >= interaction.user.top_role:
        responses = [
            "Their authority is too high for you to order a warning.",
            "Tch. Their role is equal to or above yours.",
            "Get someone with higher authority."
        ]

        await interaction.response.send_message(random.choice(responses))
        return

    if member.top_role >= interaction.guild.me.top_role:
        responses = [
            "Their role outranks mine. I can't deal with them.",
            "Tch. I don't have enough authority over them.",
            "Fix my role hierarchy first."
        ]

        await interaction.response.send_message(random.choice(responses))
        return

    db.insert(
        "warnings",
        "guild_id, user_id, moderator_id, reason, created_at",
        (
            interaction.guild.id,
            member.id,
            interaction.user.id,
            reason,
            discord.utils.utcnow().isoformat()
        )
    )

    responses = [
        f"{member.mention} has been warned. Don't make me do it again.",
        f"Tch. {member.mention}, consider this your warning.",
        f"{member.mention} has received a warning. Try not to test my patience.",
        f"Warning issued to {member.mention}. That's one mark against you."
    ]

    await interaction.response.send_message(random.choice(responses))


def setup(bot):
    bot.tree.add_command(warn)