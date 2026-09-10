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
@app_commands.default_permissions(manage_messages=True)
async def clear(
    interaction: discord.Interaction,
    amount: app_commands.Range[int, 1, 100]
):
    try:
        await interaction.response.defer()

        deleted = await interaction.channel.purge(
            limit=amount
        )

        responses = [
            f"Tch. {len(deleted)} messages are gone.",
            f"Cleaned up {len(deleted)} messages. Try keeping things tidy.",
            f"{len(deleted)} messages erased. Happy now?",
            f"Done. I removed {len(deleted)} messages from this mess."
        ]

        await interaction.followup.send(
            random.choice(responses),
            delete_after=5
        )

    except discord.Forbidden:
        responses = [
            "I don't have permission to clean this place up.",
            "Tch. Give me Manage Messages first.",
            "My authority isn't enough to remove these messages."
        ]

        if interaction.response.is_done():
            await interaction.followup.send(
                random.choice(responses)
            )
        else:
            await interaction.response.send_message(
                random.choice(responses)
            )

    except discord.HTTPException:
        responses = [
            "Something went wrong. The messages are still there.",
            "Tch. Discord rejected the cleanup.",
            "The operation failed. Try again."
        ]

        if interaction.response.is_done():
            await interaction.followup.send(
                random.choice(responses)
            )
        else:
            await interaction.response.send_message(
                random.choice(responses)
            )


def setup(bot):
    bot.tree.add_command(clear)