import random
from datetime import timedelta

import discord
from discord import app_commands


@app_commands.command(
    name="timeout",
    description="Timeout a member."
)
@app_commands.describe(
    member="The member you want to timeout.",
    duration="How long the timeout should last in minutes.",
    reason="Why the member is being timed out."
)
@app_commands.default_permissions(moderate_members=True)
async def timeout(
    interaction: discord.Interaction,
    member: discord.Member,
    duration: app_commands.Range[int, 1, 40320],
    reason: str = "No reason provided."
):
    if member.id == interaction.user.id:
        responses = [
            "You want me to silence you? Make up your mind.",
            "Tch. I'm not timing you out just because you asked.",
            "If you want silence, stop talking."
        ]

        await interaction.response.send_message(random.choice(responses))
        return

    if member.id == interaction.guild.owner_id:
        responses = [
            "I'm not timing out the owner. Even I know where the line is.",
            "You expect me to silence the owner? No.",
            "Tch. The owner's authority is above mine."
        ]

        await interaction.response.send_message(random.choice(responses))
        return

    if member.top_role >= interaction.user.top_role:
        responses = [
            "Their authority is too high. You can't order me to punish them.",
            "Tch. Their role is equal to or above yours.",
            "Get someone with higher authority if you want that done."
        ]

        await interaction.response.send_message(random.choice(responses))
        return

    if member.top_role >= interaction.guild.me.top_role:
        responses = [
            "Their role outranks mine. I can't touch them.",
            "Tch. Give me enough authority first.",
            "They're above my highest role. I can't timeout them."
        ]

        await interaction.response.send_message(random.choice(responses))
        return

    try:
        await member.timeout(
            discord.utils.utcnow() + timedelta(minutes=duration),
            reason=f"{reason} | Timed out by {interaction.user}"
        )

        responses = [
            f"{member} has been silenced for {duration} minute(s).",
            f"Tch. {member} won't be speaking for the next {duration} minute(s).",
            f"{member} is going quiet for {duration} minute(s).",
            f"Done. {member} has been put on timeout."
        ]

        await interaction.response.send_message(random.choice(responses))

    except discord.Forbidden:
        responses = [
            "I don't have enough authority to timeout them.",
            "Tch. My permissions aren't enough.",
            "I can't apply the timeout with my current authority."
        ]

        await interaction.response.send_message(random.choice(responses))

    except discord.HTTPException:
        responses = [
            "The timeout failed. Discord rejected the operation.",
            "Tch. Something went wrong. They're still talking.",
            "The operation failed. Try again."
        ]

        await interaction.response.send_message(random.choice(responses))


def setup(bot):
    bot.tree.add_command(timeout)