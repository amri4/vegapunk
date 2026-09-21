import discord

from ..buttons.square import SquareButton
from ..functions.game import create_board


class TicTacToeView(discord.ui.View):

    def __init__(self, player_x, player_o):
        super().__init__(timeout=300)

        self.player_x = player_x
        self.player_o = player_o

        self.current_player = player_x
        self.board = create_board()
        self.game_over = False

        for position in range(9):
            self.add_item(SquareButton(position))