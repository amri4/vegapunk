import discord
import mycord

from ..game import update_lobby, get_game

db = mycord.DB()


class JoinButton(discord.ui.Button):
    def __init__(self, game_id):
        super().__init__(
            label="Join",
            emoji="➕",
            style=discord.ButtonStyle.success
        )
        self.game_id = game_id
        self.callback = self.join_callback

    async def join_callback(self, interaction: discord.Interaction):
        game = get_game(self.game_id)

        if game is None:
            await interaction.response.send_message(
                "❌ This game no longer exists.",
                ephemeral=True
            )
            return

        if game[4] != "lobby":
            await interaction.response.send_message(
                "❌ This game has already started.",
                ephemeral=True
            )
            return

        exists = db.exists(
            "werewolf_players",
            "game_id = ? AND user_id = ?",
            (
                self.game_id,
                interaction.user.id
            )
        )

        if exists:
            await interaction.response.send_message(
                "❌ You are already in this game.",
                ephemeral=True
            )
            return

        db.insert(
            "werewolf_players",
            "game_id, user_id, is_bot, display_name",
            (
                self.game_id,
                interaction.user.id,
                0,
                interaction.user.display_name
            )
        )

        await update_lobby(
            interaction.message,
            self.game_id
        )

        await interaction.response.send_message(
            "🐺 You joined the game!",
            ephemeral=True
        )
