import discord
from discord import app_commands


@app_commands.command(
    name="addcategory",
    description="Create a new server category."
)
@app_commands.describe(
    name="The name of the new server category."
)
async def addcategory(
    interaction: discord.Interaction,
    name: str
):
    name = name.strip()

    if not name:
        await interaction.response.send_message(
            "❌ Please provide a category name.",
            ephemeral=True
        )
        return

    category = await interaction.guild.create_category(
        name=name,
        reason=f"Created by {interaction.user}"
    )

    await interaction.response.send_message(
        f"✅ Created category **{category.name}**."
    )


def setup(bot):
    bot.tree.add_command(addcategory)