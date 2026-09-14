import discord
from discord import app_commands

from ..functions.set_welcome import set_welcome


@app_commands.command(
    name="setwelcome",
    description="Set the welcome channel."
)
@app_commands.describe(
    channel="The channel where welcome messages will be sent."
)
@app_commands.default_permissions(manage_guild=True)
async def setwelcome(
    interaction: discord.Interaction,
    channel: discord.TextChannel
):
    set_welcome(
        interaction.guild.id,
        channel.id
    )

    await interaction.response.send_message(
        f"✅ Welcome messages will now be sent in {channel.mention}."
    )


def setup(bot):
    bot.tree.add_command(setwelcome)