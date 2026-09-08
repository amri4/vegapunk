import discord
from discord import app_commands
from .buttons.join import JoinButton

import mycord

db = mycord.DB()


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
    game = db.fetchone(
        "werewolf_games",
        "creator_id = ?",
        (interaction.user.id,)
    )
    current_game = game[0]
    db.insert(
        "werewolf_players",
        "game_id, user_id",
        (
            current_game,
            interaction.user.id
        )
    )
    players = [
        player
        for player in db.fetchall("werewolf_players")
        if player[1] == current_game
    ]
    player_count = len(players)

    player_mentions = "\n".join(
        f"<@{player[2]}>"
        for player in players
    )

    embed = discord.Embed(
        title="🐺 Werewolf game lobby",
        description="Click the buttons below to join/leave\n\n Waiting for players..."
    )
    embed.add_field(
        name="👤 Players in lobby",
        value=f"**{player_count}** player(s)\n{player_mentions}",
        inline=True
    )
    view = discord.ui.View()
    view.add_item(JoinButton(current_game))
    await interaction.response.send_message(
        embed=embed,
        view=view
    )

def setup(bot):
    bot.tree.add_command(werewolf)