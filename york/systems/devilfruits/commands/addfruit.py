import discord
from discord import app_commands

from ..functions.fruits import add_fruit


@app_commands.command(
    name="addfruit",
    description="Add a Devil Fruit to the catalog."
)
@app_commands.default_permissions(
    manage_guild=True
)
async def addfruit(
    interaction: discord.Interaction,
    fruit_id: str,
    name: str,
    emoji: str,
    rarity: str,
    sell_value: int
):
    add_fruit(
        fruit_id,
        name,
        emoji,
        rarity,
        True,
        sell_value
    )

    await interaction.response.send_message(
        f"✅ Added **{name}** to the Devil Fruit catalog."
    )


def setup(bot):
    bot.tree.add_command(
        addfruit
    )