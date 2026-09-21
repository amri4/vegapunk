import random

import discord
from discord import app_commands

from ..functions.fruits import get_fruits
from ..functions.rarity import get_rarity_weight

from ...inventory.functions.inventory import add_item
from ...berries.functions.berries import (
    get_berries,
    remove_berries
)


ROLL_COST = 1000


@app_commands.command(
    name="rollfruit",
    description="Roll for a random Devil Fruit."
)
async def rollfruit(
    interaction: discord.Interaction
):
    guild_id = interaction.guild.id
    user_id = interaction.user.id

    berries = get_berries(
        guild_id,
        user_id
    )

    if berries < ROLL_COST:
        await interaction.response.send_message(
            f"❌ You need **{ROLL_COST:,} berries** to roll a "
            f"Devil Fruit.\n"
            f"You currently have **{berries:,} berries**.",
            ephemeral=True
        )
        return

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

    remove_berries(
        guild_id,
        user_id,
        ROLL_COST
    )

    add_item(
        guild_id,
        user_id,
        fruit_id
    )

    await interaction.response.send_message(
        f"🎲 You rolled...\n\n"
        f"{emoji} **{name}**\n"
        f"✨ Rarity: **{rarity}**\n\n"
        f"Added to your inventory! 🎒\n"
        f"💰 Cost: **{ROLL_COST:,} berries**"
    )


def setup(bot):
    bot.tree.add_command(
        rollfruit
    )