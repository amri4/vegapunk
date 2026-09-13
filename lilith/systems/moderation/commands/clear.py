import random

import discord
from discord import app_commands


@app_commands.command(
    name="clear",
    description="Delete a number of messages."
)
@app_commands.describe(
    amount="The number of messages to delete."
)
@app_commands.default_permissions(
    manage_messages=True
)
async def clear(
    interaction: discord.Interaction,
    amount: app_commands.Range[int, 1, 100]
):
    await interaction.response.defer(ephemeral=True)

    try:
        # purge handles bulk deletion efficiently and catches discord.NotFound internally
        deleted = await interaction.channel.purge(limit=amount)
        deleted_count = len(deleted)

        responses = [
            f"Tch. {deleted_count} messages are gone.",
            f"Cleaned up {deleted_count} messages. Try keeping things tidy.",
            f"{deleted_count} messages erased. Happy now?",
            f"Done. I removed {deleted_count} messages from this mess."
        ]

        await interaction.followup.send(
            random.choice(responses),
            ephemeral=True
        )

    except discord.Forbidden:
        await interaction.followup.send(
            random.choice([
                "I don't have permission to clean this place up.",
                "Tch. Give me Manage Messages first.",
                "My authority isn't enough to remove these messages."
            ]),
            ephemeral=True
        )

    except discord.HTTPException:
        await interaction.followup.send(
            random.choice([
                "Something went wrong. The messages are still there.",
                "Tch. Discord rejected the cleanup.",
                "The operation failed. Try again."
            ]),
            ephemeral=True
        )

def setup(bot):
    bot.tree.add_command(clear)
