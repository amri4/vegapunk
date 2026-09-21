import random

import discord
from discord import app_commands

from ..functions.fruits import get_fruits
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

    fruit = random.choice(
        fruits
    )

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