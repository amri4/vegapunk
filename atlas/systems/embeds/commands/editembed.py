import discord
from discord import app_commands

from ..functions.edit_embed import edit_embed


@app_commands.command(
    name="editembed",
    description="Edit an existing embed."
)
@app_commands.describe(
    message_id="The ID of the embed message.",
    title="New title.",
    description="New description.",
    color="New embed color.",
    image="New image.",
    thumbnail="New thumbnail."
)
@app_commands.default_permissions(manage_messages=True)
async def editembed(
    interaction: discord.Interaction,
    message_id: str,
    title: str | None = None,
    description: str | None = None,
    color: str | None = None,
    image: discord.Attachment | None = None,
    thumbnail: discord.Attachment | None = None
):
    await edit_embed(
        interaction,
        message_id,
        title,
        description,
        color,
        image,
        thumbnail
    )


def setup(bot):
    bot.tree.add_command(editembed)