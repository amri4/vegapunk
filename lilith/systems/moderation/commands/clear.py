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
        messages = []

        async for message in interaction.channel.history(
            limit=amount
        ):
            messages.append(message)

        await interaction.response.defer()

        if messages:
            await interaction.channel.delete_messages(
                messages
            )

        responses = [
            f"Tch. {len(messages)} messages are gone.",
            f"Cleaned up {len(messages)} messages. Try keeping things tidy.",
            f"{len(messages)} messages erased. Happy now?",
            f"Done. I removed {len(messages)} messages from this mess."
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

        await interaction.followup.send(
            random.choice(responses)
        )

    except discord.HTTPException:
        responses = [
            "Something went wrong. The messages are still there.",
            "Tch. Discord rejected the cleanup.",
            "The operation failed. Try again."
        ]

        await interaction.followup.send(
            random.choice(responses)
        )


def setup(bot):
    bot.tree.add_command(clear)