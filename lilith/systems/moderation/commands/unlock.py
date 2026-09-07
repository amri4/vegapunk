import random

import discord
from discord import app_commands


@app_commands.command(
    name="unlock",
    description="Unlock a channel so members can send messages."
)
@app_commands.describe(
    channel="The channel you want to unlock."
)
@app_commands.default_permissions(manage_channels=True)
async def unlock(
    interaction: discord.Interaction,
    channel: discord.TextChannel
):
    overwrite = channel.overwrites_for(interaction.guild.default_role)

    if overwrite.send_messages is not False:
        responses = [
            "Tch. This channel isn't locked.",
            "It's already open. What exactly am I supposed to unlock?",
            "Nobody sealed this place in the first place."
        ]

        await interaction.response.send_message(random.choice(responses))
        return

    overwrite.send_messages = None

    try:
        await channel.set_permissions(
            interaction.guild.default_role,
            overwrite=overwrite,
            reason=f"Channel unlocked by {interaction.user}"
        )

        responses = [
            f"🔓 {channel.mention} is open again. Try not to cause another mess.",
            f"{channel.mention} has been unlocked. You're free to talk again.",
            f"Tch. {channel.mention} is no longer under lockdown.",
            f"🔓 Done. {channel.mention} is open."
        ]

        await interaction.response.send_message(random.choice(responses))

    except discord.Forbidden:
        responses = [
            "I don't have enough authority to unlock that channel.",
            "Tch. Give me Manage Channels first.",
            "My permissions aren't enough to open that channel."
        ]

        await interaction.response.send_message(random.choice(responses))

    except discord.HTTPException:
        responses = [
            "Something went wrong. The channel is still locked.",
            "Tch. Discord rejected the operation.",
            "The operation failed. Try again."
        ]

        await interaction.response.send_message(random.choice(responses))


def setup(bot):
    bot.tree.add_command(unlock)