import random

import discord
from discord import app_commands


@app_commands.command(
    name="slowmode",
    description="Set the slowmode delay for a channel."
)
@app_commands.describe(
    channel="The channel you want to change.",
    seconds="The delay between messages in seconds. Use 0 to disable slowmode."
)
@app_commands.default_permissions(manage_channels=True)
async def slowmode(
    interaction: discord.Interaction,
    channel: discord.TextChannel,
    seconds: app_commands.Range[int, 0, 21600]
):
    try:
        await channel.edit(
            slowmode_delay=seconds,
            reason=f"Slowmode changed by {interaction.user}"
        )

        if seconds == 0:
            responses = [
                f"⏱️ Slowmode is off in {channel.mention}. Try not to flood it.",
                f"{channel.mention} is back to normal speed.",
                f"Tch. I removed the slowmode from {channel.mention}."
            ]
        else:
            responses = [
                f"⏱️ Slowmode set to {seconds} seconds in {channel.mention}.",
                f"{channel.mention} now has a {seconds}-second delay. Slow down.",
                f"Tch. {channel.mention} will be waiting {seconds} seconds between messages."
            ]

        await interaction.response.send_message(
            random.choice(responses)
        )

    except discord.Forbidden:
        responses = [
            "I don't have enough authority to change that channel.",
            "Tch. Give me Manage Channels first.",
            "My permissions aren't enough for this."
        ]

        await interaction.response.send_message(
            random.choice(responses)
        )

    except discord.HTTPException:
        responses = [
            "Something went wrong. The slowmode wasn't changed.",
            "Tch. Discord rejected the operation.",
            "The operation failed. Try again."
        ]

        await interaction.response.send_message(
            random.choice(responses)
        )


def setup(bot):
    bot.tree.add_command(slowmode)