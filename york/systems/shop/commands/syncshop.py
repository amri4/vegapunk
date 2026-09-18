import discord
from discord import app_commands

from ..functions.sync import sync_shop


@app_commands.command(
    name="syncshop",
    description="Sync the shop with its current items."
)
@app_commands.default_permissions(manage_guild=True)
async def syncshop(interaction: discord.Interaction):
    await sync_shop(
        interaction.client
    )

    await interaction.response.send_message(
        "✅ Shop synced successfully."
    )


def setup(bot):
    bot.tree.add_command(
        syncshop
    )