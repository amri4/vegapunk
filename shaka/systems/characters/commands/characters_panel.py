import discord
from discord import app_commands

import mycord

from ..functions.update_panel import update_panel


db = mycord.DB()


@app_commands.command(
    name="characters_panel",
    description="Create the character claims panel."
)
@app_commands.default_permissions(manage_guild=True)
async def characters_panel(
    interaction: discord.Interaction
):
    if interaction.guild is None:
        return await interaction.response.send_message(
            "❌ This command can only be used in a server."
        )

    existing = db.fetchone(
        "character_panels",
        "guild_id = ?",
        (interaction.guild.id,)
    )

    if existing is not None:
        channel = interaction.client.get_channel(existing[1])

        if channel is not None:
            try:
                message = await channel.fetch_message(existing[2])

                await interaction.response.send_message(
                    "❌ A character panel already exists."
                )
                return

            except discord.NotFound:
                pass

    embed = discord.Embed(
        title="🏴‍☠️ Character Claims",
        description="No characters have been claimed yet.",
        color=discord.Color.gold()
    )

    message = await interaction.channel.send(embed=embed)

    if existing is None:
        db.insert(
            "character_panels",
            "guild_id, channel_id, message_id",
            (
                interaction.guild.id,
                interaction.channel.id,
                message.id
            )
        )
    else:
        db.update(
            "character_panels",
            "channel_id = ?, message_id = ?",
            "guild_id = ?",
            (
                interaction.channel.id,
                message.id,
                interaction.guild.id
            )
        )

    await interaction.response.send_message(
        "✅ Character panel created."
    )


def setup(bot):
    bot.tree.add_command(characters_panel)