import discord

from ..buttons.join import JoinButton
from ..buttons.leave import LeaveButton
from ..buttons.start import StartButton


class LobbyView(discord.ui.View):
    def __init__(self, game_id):
        super().__init__(timeout=None)

        self.add_item(JoinButton(game_id))
        self.add_item(LeaveButton(game_id))
        self.add_item(StartButton(game_id))
