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
    await interaction.response.defer()

    try:
        messages = [
            message
            async for message in interaction.channel.history(
                limit=amount
            )
        ]

        deleted = 0

        for message in messages:
            try:
                await message.delete()
                deleted += 1

            except discord.NotFound:
                pass

        responses = [
            f"Tch. {deleted} messages are gone.",
            f"Cleaned up {deleted} messages. Try keeping things tidy.",
            f"{deleted} messages erased. Happy now?",
            f"Done. I removed {deleted} messages from this mess."
        ]

        await interaction.followup.send(
            random.choice(responses),
            delete_after=5
        )

    except discord.Forbidden:
        await interaction.followup.send(
            random.choice([
                "I don't have permission to clean this place up.",
                "Tch. Give me Manage Messages first.",
                "My authority isn't enough to remove these messages."
            ])
        )

    except discord.HTTPException:
        await interaction.followup.send(
            random.choice([
                "Something went wrong. The messages are still there.",
                "Tch. Discord rejected the cleanup.",
                "The operation failed. Try again."
            ])
        )


def setup(bot):
    bot.tree.add_command(clear)