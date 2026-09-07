import discord
from discord import app_commands


@app_commands.command(
    name="movecategory",
    description="Move a category above or below another category."
)
@app_commands.describe(
    category="The category you want to move.",
    direction="Move it above or below the target.",
    target="The category to move relative to."
)
@app_commands.choices(
    direction=[
        app_commands.Choice(
            name="Above",
            value="above"
        ),
        app_commands.Choice(
            name="Below",
            value="below"
        )
    ]
)
async def movecategory(
    interaction: discord.Interaction,
    category: discord.CategoryChannel,
    direction: app_commands.Choice[str],
    target: discord.CategoryChannel
):
    if category.id == target.id:
        await interaction.response.send_message(
            "❌ You can't move a category relative to itself.",
            ephemeral=True
        )
        return

    target_position = target.position

    if direction.value == "above":
        new_position = target_position
    else:
        new_position = target_position + 1

    await category.edit(
        position=new_position,
        reason=f"Moved by {interaction.user}"
    )

    await interaction.response.send_message(
        f"📁 Moved category **{category.name}** "
        f"**{direction.value}** **{target.name}**."
    )


def setup(bot):
    bot.tree.add_command(movecategory)