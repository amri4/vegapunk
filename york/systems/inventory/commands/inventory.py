import discord
from discord import app_commands

from ...berries.functions.berries import get_berries
from ..functions.inventory import get_inventory


@app_commands.command(
    name="inventory",
    description="View your inventory."
)
async def inventory(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    user_id = interaction.user.id

    berries = get_berries(
        guild_id,
        user_id
    )

    items = get_inventory(
        guild_id,
        user_id
    )

    description = (
        f"<:berries:1550458400800776344> **Berries:** {berries:,}\n\n"
    )

    if not items:
        description += "🎒 Your inventory is empty."

    else:
        for item in items:
            item_id = item[2]
            amount = item[3]

            description += (
                f"• **{item_id}** ×{amount}\n"
            )

    embed = discord.Embed(
        title=f"🎒 {interaction.user.display_name}'s Inventory",
        description=description
    )

    await interaction.response.send_message(
        embed=embed
    )


def setup(bot):
    bot.tree.add_command(
        inventory
    )