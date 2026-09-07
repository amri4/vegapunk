import random

import discord
from discord import app_commands


@app_commands.command(
    name="untimeout",
    description="Remove a timeout from a member."
)
@app_commands.describe(
    member="The member whose timeout you want to remove."
)
@app_commands.default_permissions(moderate_members=True)
async def untimeout(
    interaction: discord.Interaction,
    member: discord.Member
):
    if member.id == interaction.user.id:
        responses = [
            "You timed yourself out and now want me to undo it? Make up your mind.",
            "Tch. You got yourself into this. Get yourself out.",
            "I'm not undoing your own punishment for you."
        ]

        await interaction.response.send_message(random.choice(responses))
        return

    if member.id == interaction.guild.owner_id:
        responses = [
            "The owner doesn't need me to interfere with their timeout.",
            "Tch. I'm not touching the owner's moderation status.",
            "That's the owner. Handle it yourself."
        ]

        await interaction.response.send_message(random.choice(responses))
        return

    if member.top_role >= interaction.user.top_role:
        responses = [
            "Their authority is too high. You can't order me to change their moderation status.",
            "Tch. Their role is equal to or above yours.",
            "Get someone with higher authority."
        ]

        await interaction.response.send_message(random.choice(responses))
        return

    if member.top_role >= interaction.guild.me.top_role:
        responses = [
            "Their role outranks mine. I can't change their timeout.",
            "Tch. I don't have enough authority over them.",
            "Their authority exceeds mine. Fix my permissions first."
        ]

        await interaction.response.send_message(random.choice(responses))
        return

    try:
        await member.timeout(
            None,
            reason=f"Timeout removed by {interaction.user}"
        )

        responses = [
            f"{member} can speak again.",
            f"Tch. {member}'s silence is over.",
            f"{member} has been released.",
            f"Done. {member} is no longer muted by timeout."
        ]

        await interaction.response.send_message(random.choice(responses))

    except discord.Forbidden:
        responses = [
            "I don't have enough authority to remove that timeout.",
            "Tch. My permissions aren't enough.",
            "I can't change their moderation status."
        ]

        await interaction.response.send_message(random.choice(responses))

    except discord.HTTPException:
        responses = [
            "Something went wrong. The timeout is still active.",
            "Tch. Discord rejected the operation.",
            "The operation failed. Try again."
        ]

        await interaction.response.send_message(random.choice(responses))


def setup(bot):
    bot.tree.add_command(untimeout)