import discord
from discord import app_commands


@app_commands.command(
    name="delchannel",
    description="Delete a channel."
)
@app_commands.describe(
    channel="The channel to delete."
)
async def delchannel(
    interaction: discord.Interaction,
    channel: discord.TextChannel
):
    channel_name = channel.name

    await channel.delete(
        reason=f"Deleted by {interaction.user}"
    )

    await interaction.response.send_message(
        f"✅ Deleted **{channel_name}**."
    )


def setup(bot):
    bot.tree.add_command(delchannel)