import discord
from discord import app_commands

import mycord

db = mycord.DB()


@app_commands.command(
    name="createpanel",
    description="Create a ticket panel"
)
@app_commands.describe(
    title="The title of the ticket panel",
    description="The description of the ticket panel",
    image="Panel image (optional)",
    thumbnail="Panel thumbnail (optional)"
)
async def createpanel(
    interaction: discord.Interaction,
    title: str,
    description: str,
    image: discord.Attachment | None = None,
    thumbnail: discord.Attachment | None = None
):

    config = db.fetchone(
        "server_config",
        "guild_id = ?",
        (interaction.guild.id,)
    )

    if config is None:
        await interaction.response.send_message(
            "❌ There is no server configuration. Go ask Pythagoras.",
            ephemeral=True
        )
        return

    channel_id = config[4]

    if channel_id is None:
        await interaction.response.send_message(
            "❌ There is no ticket panel channel configured. Go ask Pythagoras.",
            ephemeral=True
        )
        return

    channel = interaction.guild.get_channel(channel_id)

    if channel is None:
        await interaction.response.send_message(
            "❌ The configured ticket panel channel no longer exists.",
            ephemeral=True
        )
        return

    image_url = image.url if image else None
    thumbnail_url = thumbnail.url if thumbnail else None

    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.blue()
    )

    if image_url:
        embed.set_image(url=image_url)

    if thumbnail_url:
        embed.set_thumbnail(url=thumbnail_url)

    message = await channel.send(embed=embed)

    db.insert(
        "ticket_panels",
        """
        guild_id,
        message_id,
        title,
        description,
        image_url,
        thumbnail_url
        """,
        (
            interaction.guild.id,
            message.id,
            title,
            description,
            image_url,
            thumbnail_url
        )
    )

    panel = db.fetchone(
        "ticket_panels",
        "message_id = ?",
        (message.id,)
    )

    panel_id = panel[0]

    embed.set_footer(
        text=f"PANEL_ID: {panel_id}"
    )

    await message.edit(embed=embed)

    await interaction.response.send_message(
        "✅ Ticket panel created.",
        ephemeral=True
    )


def setup(bot):
    bot.tree.add_command(createpanel)