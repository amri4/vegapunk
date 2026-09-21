import random

import discord
from discord import app_commands

from ..functions.fruits import get_fruits
from ..functions.rarity import get_rarity_weight
from ...inventory.functions.inventory import add_item


@app_commands.command(
    name="rollfruit",
    description="Roll for a random Devil Fruit."
)
async def rollfruit(
    interaction: discord.Interaction
):
    fruits = get_fruits()

    if not fruits:
        await interaction.response.send_message(
            "❌ There are no Devil Fruits available to roll."
        )
        return

    weighted_fruits = [
        fruit
        for fruit in fruits
        if get_rarity_weight(fruit[3]) > 0
    ]

    if not weighted_fruits:
        await interaction.response.send_message(
            "❌ There are no valid Devil Fruits available to roll."
        )
        return

    weights = [
        get_rarity_weight(fruit[3])
        for fruit in weighted_fruits
    ]

    fruit = random.choices(
        weighted_fruits,
        weights=weights,
        k=1
    )[0]

    fruit_id = fruit[0]
    name = fruit[1]
    emoji = fruit[2]
    rarity = fruit[3]

    add_item(
        interaction.guild.id,
        interaction.user.id,
        fruit_id
    )

    await interaction.response.send_message(
        f"🎲 You rolled...\n\n"
        f"{emoji} **{name}**\n"
        f"✨ Rarity: **{rarity}**\n\n"
        f"Added to your inventory! 🎒"
    )


def setup(bot):
    bot.tree.add_command(
        rollfruit
    )