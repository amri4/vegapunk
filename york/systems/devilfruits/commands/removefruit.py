import discord
from discord import app_commands

from ..functions.fruits import get_fruit, remove_fruit


@app_commands.command(
    name="removefruit",
    description="Remove a Devil Fruit from the catalog."
)
@app_commands.default_permissions(
    manage_guild=True
)
async def removefruit(
    interaction: discord.Interaction,
    fruit_id: str
):
    fruit = get_fruit(
        fruit_id
    )

    if fruit is None:
        await interaction.response.send_message(
            "❌ That Devil Fruit doesn't exist."
        )
        return

    remove_fruit(
        fruit_id
    )

    await interaction.response.send_message(
        f"✅ Removed **{fruit[1]}** from the Devil Fruit catalog."
    )


def setup(bot):
    bot.tree.add_command(
        removefruit
    )