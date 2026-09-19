import discord
from discord import app_commands

from ..functions.sync import sync_shop


@app_commands.command(
    name="syncshop",
    description="Sync the shop."
)
@app_commands.default_permissions(manage_guild=True)
async def syncshop(interaction: discord.Interaction):
    try:
        await sync_shop(
            interaction.client,
            interaction.guild
        )

        await interaction.response.send_message(
            "✅ Shop synced successfully."
        )

    except Exception as error:
        await interaction.response.send_message(
            f"❌ Error: `{error}`",
            ephemeral=True
        )


def setup(bot):
    bot.tree.add_command(syncshop)