import random

import discord
from discord import app_commands


@app_commands.command(
    name="lock",
    description="Lock a channel so members cannot send messages."
)
@app_commands.describe(
    channel="The channel you want to lock."
)
@app_commands.default_permissions(manage_channels=True)
async def lock(
    interaction: discord.Interaction,
    channel: discord.TextChannel
):
    overwrite = channel.overwrites_for(interaction.guild.default_role)

    if overwrite.send_messages is False:
        responses = [
            "Tch. This channel is already locked.",
            "It's already sealed. Try paying attention.",
            "This place is already under lockdown."
        ]

        await interaction.response.send_message(random.choice(responses))
        return

    overwrite.send_messages = False

    try:
        await channel.set_permissions(
            interaction.guild.default_role,
            overwrite=overwrite,
            reason=f"Channel locked by {interaction.user}"
        )

        responses = [
            f"🔒 {channel.mention} is locked. Nobody's talking here until I say so.",
            f"{channel.mention} has been sealed. Keep everyone quiet.",
            f"Tch. {channel.mention} is under lockdown.",
            f"🔒 Locked. {channel.mention} is off-limits."
        ]

        await interaction.response.send_message(random.choice(responses))

    except discord.Forbidden:
        responses = [
            "I don't have enough authority to lock that channel.",
            "Tch. Give me Manage Channels first.",
            "My permissions aren't enough to seal that channel."
        ]

        await interaction.response.send_message(random.choice(responses))

    except discord.HTTPException:
        responses = [
            "Something went wrong. The channel is still open.",
            "Tch. Discord rejected the lockdown.",
            "The operation failed. Try again."
        ]

        await interaction.response.send_message(random.choice(responses))


def setup(bot):
    bot.tree.add_command(lock)