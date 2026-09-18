import discord
from discord import app_commands

from ..functions.shop import set_shop_channel


@app_commands.command(
    name="shopchannel",
    description="Set the channel where the shop will appear."
)
@app_commands.default_permissions(
    manage_guild=True
)
async def shopchannel(
    interaction: discord.Interaction,
    channel: discord.TextChannel
):
    set_shop_channel(
        interaction.guild.id,
        channel.id
    )

    await interaction.response.send_message(
        f"✅ Shop channel set to {channel.mention}."
    )


def setup(bot):
    bot.tree.add_command(
        shopchannel
    )