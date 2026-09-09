import discord
import mycord

from ..game import update_lobby, get_game

db = mycord.DB()


class LeaveButton(discord.ui.Button):
    def __init__(self, game_id):
        super().__init__(
            label="Leave",
            emoji="➖",
            style=discord.ButtonStyle.danger
        )
        self.game_id = game_id
        self.callback = self.leave_callback

    async def leave_callback(self, interaction: discord.Interaction):
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

        if interaction.user.id == game[3]:
            await interaction.response.send_message(
                "❌ The creator cannot leave their own lobby.",
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

        if not exists:
            await interaction.response.send_message(
                "❌ You are not in this game.",
                ephemeral=True
            )
            return

        db.delete(
            "werewolf_players",
            "game_id = ? AND user_id = ?",
            (
                self.game_id,
                interaction.user.id
            )
        )

        await update_lobby(
            interaction.message,
            self.game_id
        )

        await interaction.response.send_message(
            "👋 You left the game.",
            ephemeral=True
        )
