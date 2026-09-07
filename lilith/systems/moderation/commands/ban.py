import random

import discord
from discord import app_commands


@app_commands.command(
    name="ban",
    description="Ban a member from the server."
)
@app_commands.describe(
    member="The member you want to ban.",
    reason="Why the member is being banned."
)
@app_commands.default_permissions(ban_members=True)
async def ban(
    interaction: discord.Interaction,
    member: discord.Member,
    reason: str = "No reason provided."
):
    if member.id == interaction.user.id:
        responses = [
            "You want to ban yourself? Tch. I'm not doing that.",
            "Seriously? You're asking me to remove you?",
            "I'm not banning you. Find a better use of my time."
        ]

        await interaction.response.send_message(
            responses[random.randint(0, len(responses) - 1)]
        )
        return

    if member.id == interaction.guild.owner_id:
        responses = [
            "I'm not touching the owner. Even I know better than that.",
            "You expect me to ban the person who owns this place? No.",
            "Tch. That's the server owner. Find someone else."
        ]

        await interaction.response.send_message(
            responses[random.randint(0, len(responses) - 1)]
        )
        return

    if member.top_role >= interaction.user.top_role:
        responses = [
            "Their authority is too high. You can't expect me to override yours.",
            "Tch. Your authority doesn't exceed theirs. I can't ban them.",
            "They're above your rank. Get someone with enough authority."
        ]

        await interaction.response.send_message(
            responses[random.randint(0, len(responses) - 1)]
        )
        return

    if member.top_role >= interaction.guild.me.top_role:
        responses = [
            "They're above my authority. Fix my permissions if you want this done.",
            "Tch. Their role is higher than mine. I can't remove them.",
            "My authority isn't high enough to deal with them."
        ]

        await interaction.response.send_message(
            responses[random.randint(0, len(responses) - 1)]
        )
        return

    try:
        await member.ban(
            reason=f"{reason} | Banned by {interaction.user}"
        )

        responses = [
            f"{member} is gone. Problem solved.",
            f"Tch. {member} has been removed.",
            f"Consider {member} erased from this island.",
            f"Done. {member} won't be causing trouble here anymore."
        ]

        await interaction.response.send_message(
            responses[random.randint(0, len(responses) - 1)]
        )

    except discord.Forbidden:
        responses = [
            "I don't have enough authority to do that.",
            "Tch. My permissions aren't enough.",
            "You gave me the job but not the authority. Fix it."
        ]

        await interaction.response.send_message(
            responses[random.randint(0, len(responses) - 1)]
        )

    except discord.HTTPException:
        responses = [
            "Something went wrong. The ban didn't go through.",
            "Tch. Discord rejected the operation.",
            "The operation failed. Try again."
        ]

        await interaction.response.send_message(
            responses[random.randint(0, len(responses) - 1)]
        )


def setup(bot):
    bot.tree.add_command(ban)