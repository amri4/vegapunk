import discord
from discord import app_commands

from ..functions.embed_setup import start_embed_setup


@app_commands.command(
    name="sendembed",
    description="Create and send an interactive embed."
)
@app_commands.describe(
    channel="The channel where the embed will be sent."
)
@app_commands.default_permissions(manage_messages=True)
async def sendembed(
    interaction: discord.Interaction,
    channel: discord.TextChannel
):
    await start_embed_setup(
        interaction,
        channel
    )


def setup(bot):
    bot.tree.add_command(sendembed)