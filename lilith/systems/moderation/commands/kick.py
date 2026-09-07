import random

import discord
from discord import app_commands


@app_commands.command(
    name="kick",
    description="Kick a member from the server."
)
@app_commands.describe(
    member="The member you want to kick.",
    reason="Why the member is being kicked."
)
@app_commands.default_permissions(kick_members=True)
async def kick(
    interaction: discord.Interaction,
    member: discord.Member,
    reason: str = "No reason provided."
):
    if member.id == interaction.user.id:
        responses = [
            "You want me to kick you? Tch. I'm not playing along.",
            "You're asking me to throw you out? Ridiculous.",
            "No. I'm not kicking you. Try using your authority properly."
        ]

        await interaction.response.send_message(random.choice(responses))
        return

    if member.id == interaction.guild.owner_id:
        responses = [
            "I'm not kicking the owner. Even I have limits.",
            "You want me to throw out the person who owns this place? No.",
            "Tch. That's the owner. Find someone else."
        ]

        await interaction.response.send_message(random.choice(responses))
        return

    if member.top_role >= interaction.user.top_role:
        responses = [
            "Their authority is too high for you to order their removal.",
            "Tch. Their role is equal to or above yours. I can't kick them.",
            "They're above your authority. Get someone with a higher rank."
        ]

        await interaction.response.send_message(random.choice(responses))
        return

    if member.top_role >= interaction.guild.me.top_role:
        responses = [
            "They're above my authority. Give me a higher role.",
            "Tch. I can't kick someone whose role outranks mine.",
            "My authority isn't high enough to remove them."
        ]

        await interaction.response.send_message(random.choice(responses))
        return

    try:
        await member.kick(
            reason=f"{reason} | Kicked by {interaction.user}"
        )

        responses = [
            f"{member} has been thrown out.",
            f"Tch. {member} is out.",
            f"{member} has been removed from this island.",
            f"Done. {member} is no longer a problem here."
        ]

        await interaction.response.send_message(random.choice(responses))

    except discord.Forbidden:
        responses = [
            "I don't have enough authority to kick them.",
            "Tch. My permissions aren't enough.",
            "You gave me the job, but not enough authority to carry it out."
        ]

        await interaction.response.send_message(random.choice(responses))

    except discord.HTTPException:
        responses = [
            "The kick failed. Discord rejected the operation.",
            "Tch. Something went wrong. They're still here.",
            "The operation failed. Try again."
        ]

        await interaction.response.send_message(random.choice(responses))


def setup(bot):
    bot.tree.add_command(kick)