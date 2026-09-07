import discord
from discord import app_commands


@app_commands.command(
    name="delcategory",
    description="Delete a server category."
)
@app_commands.describe(
    category="The category to delete."
)
async def delcategory(
    interaction: discord.Interaction,
    category: discord.CategoryChannel
):
    category_name = category.name

    await category.delete(
        reason=f"Deleted by {interaction.user}"
    )

    await interaction.response.send_message(
        f"🗑️ Deleted category **{category_name}**."
    )


def setup(bot):
    bot.tree.add_command(delcategory)