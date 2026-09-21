import discord
from discord import app_commands

from ..functions.fruits import (
    get_fruit,
    get_fruits,
    remove_fruit
)

from ...inventory.functions.inventory import (
    remove_item_everywhere
)


async def fruit_autocomplete(
    interaction: discord.Interaction,
    current: str
):
    fruits = get_fruits()

    current = current.lower()

    choices = []

    for fruit in fruits:

        fruit_id = fruit[0]
        name = fruit[1]
        emoji = fruit[2]

        if current not in name.lower():
            continue

        choices.append(
            app_commands.Choice(
                name=f"{emoji} {name}",
                value=fruit_id
            )
        )

        if len(choices) >= 25:
            break

    return choices


@app_commands.command(
    name="removefruit",
    description="Remove a Devil Fruit from the catalog."
)
@app_commands.default_permissions(
    manage_guild=True
)
@app_commands.autocomplete(
    fruit=fruit_autocomplete
)
async def removefruit(
    interaction: discord.Interaction,
    fruit: str
):
    fruit_data = get_fruit(
        fruit
    )

    if fruit_data is None:
        await interaction.response.send_message(
            "❌ That Devil Fruit doesn't exist in the catalog.",
            ephemeral=True
        )
        return

    fruit_name = fruit_data[1]
    fruit_emoji = fruit_data[2]

    remove_fruit(
        fruit
    )

    remove_item_everywhere(
        fruit
    )

    await interaction.response.send_message(
        f"✅ Removed {fruit_emoji} **{fruit_name}** "
        "from the Devil Fruit catalog and all inventories."
    )


def setup(bot):
    bot.tree.add_command(
        removefruit
    )