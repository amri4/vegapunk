import discord
from discord import app_commands

from ..functions.faction_panel import send_faction_panel


@app_commands.command(
    name="factionpanel",
    description="Send the Pirate and Marine faction panel."
)
@app_commands.default_permissions(administrator=True)
async def factionpanel(interaction: discord.Interaction):
    await send_faction_panel(interaction)


def setup(bot):
    bot.tree.add_command(factionpanel)
