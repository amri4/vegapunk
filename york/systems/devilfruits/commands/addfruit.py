import re

import discord
from discord import app_commands

from ..functions.fruits import add_fruit


RARITIES = [
    "Common",
    "Uncommon",
    "Rare",
    "Epic",
    "Legendary"
]


def create_fruit_id(name):
    fruit_id = name.lower()

    fruit_id = re.sub(
        r"[^a-z0-9]+",
        "_",
        fruit_id
    )

    fruit_id = fruit_id.strip("_")

    return fruit_id


@app_commands.command(
    name="addfruit",
    description="Add a Devil Fruit to the catalog."
)
@app_commands.default_permissions(
    manage_guild=True
)
@app_commands.choices(
    rarity=[
        app_commands.Choice(
            name=rarity,
            value=rarity
        )
        for rarity in RARITIES
    ]
)
async def addfruit(
    interaction: discord.Interaction,
    name: str,
    emoji: str,
    rarity: app_commands.Choice[str],
    sell_value: int
):
    fruit_id = create_fruit_id(
        name
    )

    add_fruit(
        fruit_id,
        name,
        emoji,
        rarity.value,
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