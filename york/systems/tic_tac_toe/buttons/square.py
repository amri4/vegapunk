import discord

from ..functions.game import make_move, check_winner, game_over


class SquareButton(discord.ui.Button):

    def __init__(self, position):
        super().__init__(
            label=" ",
            style=discord.ButtonStyle.secondary,
            row=position // 3
        )

        self.position = position

    async def callback(self, interaction):
        view = self.view

        if view.game_over:
            await interaction.response.send_message(
                "❌ This game is already over.",
                ephemeral=True
            )
            return

        if interaction.user.id not in (
            view.player_x,
            view.player_o
        ):
            await interaction.response.send_message(
                "❌ You're not part of this game.",
                ephemeral=True
            )
            return

        if interaction.user.id != view.current_player:
            await interaction.response.send_message(
                "⏳ It's not your turn.",
                ephemeral=True
            )
            return

        symbol = "❌" if interaction.user.id == view.player_x else "⭕"

        if not make_move(view.board, self.position, symbol):
            await interaction.response.send_message(
                "❌ That square is already taken.",
                ephemeral=True
            )
            return

        self.label = symbol
        self.disabled = True

        winner = check_winner(view.board)

        if winner is not None:
            view.game_over = True

            for button in view.children:
                button.disabled = True

            await interaction.response.edit_message(
                content=f"🏆 **{winner} wins!**",
                view=view
            )
            return

        if game_over(view.board):
            view.game_over = True

            for button in view.children:
                button.disabled = True

            await interaction.response.edit_message(
                content="🤝 **It's a draw!**",
                view=view
            )
            return

        if interaction.user.id == view.player_x:
            view.current_player = view.player_o
        else:
            view.current_player = view.player_x

        await interaction.response.edit_message(view=view)