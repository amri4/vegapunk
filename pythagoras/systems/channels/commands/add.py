import discord
from discord import app_commands

from ..functions.find_category import find_category


@app_commands.command(
    name="addchannel",
    description="Create a text channel inside a category."
)
@app_commands.describe(
    category="The category to create the channel in.",
    name="The name of the new text channel."
)
async def addchannel(
    interaction: discord.Interaction,
    category: str,
    name: str
):
    category_obj, error = find_category(
        interaction.guild,
        category
    )

    if error:
        await interaction.response.send_message(error, ephemeral=True)
        return

    channel = await interaction.guild.create_text_channel(
        name=name,
        category=category_obj
    )

    await interaction.response.send_message(
        f"✅ Created {channel.mention} in **{category_obj.name}**."
    )


def setup(bot):
    bot.tree.add_command(addchannel)