import discord
from discord import app_commands

import mycord

from .views.lobby import LobbyView

db = mycord.DB()


@app_commands.command(
    name="werewolf",
    description="Play the Werewolf game"
)
@app_commands.describe(
    werewolves="Number of werewolves",
    seers="Number of seers",
    doctors="Number of doctors"
)
async def werewolf(
    interaction: discord.Interaction,
    werewolves: int,
    seers: int,
    doctors: int
):
    try:
        if interaction.guild is None:
            await interaction.response.send_message(
                "❌ This command can only be used in a server.",
                ephemeral=True
            )
            return

        if werewolves < 1 or seers < 0 or doctors < 0:
            await interaction.response.send_message(
                "❌ Role counts are invalid.",
                ephemeral=True
            )
            return

        existing = db.fetchone(
            "werewolf_games",
            "guild_id = ? AND creator_id = ?",
            (
                interaction.guild.id,
                interaction.user.id
            )
        )

        if existing is not None:
            await interaction.response.send_message(
                "❌ You already have a Werewolf game.",
                ephemeral=True
            )
            return

        db.insert(
            "werewolf_games",
            "guild_id, channel_id, creator_id, werewolves, seers, doctors",
            (
                interaction.guild.id,
                interaction.channel.id,
                interaction.user.id,
                werewolves,
                seers,
                doctors
            )
        )

        game = db.fetchone(
            "werewolf_games",
            "guild_id = ? AND creator_id = ?",
            (
                interaction.guild.id,
                interaction.user.id
            )
        )

        if game is None:
            await interaction.response.send_message(
                "❌ Failed to create the game.",
                ephemeral=True
            )
            return

        game_id = game[0]

        db.insert(
            "werewolf_players",
            "game_id, user_id, is_bot, display_name",
            (
                game_id,
                interaction.user.id,
                0,
                interaction.user.display_name
            )
        )

        embed = discord.Embed(
            title="🐺 Werewolf game lobby",
            description="Click the buttons below to join or leave."
        )

        embed.add_field(
            name="👤 Players",
            value=f"**1 player(s)**\n<@{interaction.user.id}>",
            inline=False
        )

        embed.add_field(
            name="⚙️ Roles",
            value=(
                f"🐺 Werewolves: **{werewolves}**\n"
                f"🔮 Seers: **{seers}**\n"
                f"🩺 Doctors: **{doctors}**"
            ),
            inline=False
        )

        await interaction.response.send_message(
            embed=embed,
            view=LobbyView(game_id)
        )

    except Exception as e:
        error = f"❌ **Werewolf error**\n`{type(e).__name__}: {e}`"

        if interaction.response.is_done():
            await interaction.followup.send(
                error,
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                error,
                ephemeral=True
            )


def setup(bot):
    bot.tree.add_command(werewolf)