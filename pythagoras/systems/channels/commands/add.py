import discord
from discord import app_commands


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
    category: discord.CategoryChannel,
    name: str
):
    channel = await interaction.guild.create_text_channel(
        name=name,
        category=category
    )

    await interaction.response.send_message(
        f"✅ Created {channel.mention} in **{category.name}**."
    )


def setup(bot):
    bot.tree.add_command(addchannel)