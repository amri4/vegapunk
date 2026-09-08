import discord
from discord import app_commands

import mycord

db = mycord.DB()

@app_commands.describe(
    players="Select players joining the game"
)
@app_commands.command(
    name="werewolf",
    description="play the werewolf game"
)
async def werewolf(
    interaction: discord.Interaction
):
    db.insert(
        "werewolf_games",
        "guild_id, channel_id, creator_id",
        (
            interaction.guild.id,
            interaction.channel.id,
            interaction.user.id
        )
    )
    await interaction.response.send_message(
        "Game worked!"
    )

def setup(bot):
    bot.tree.add_command(werewolf)