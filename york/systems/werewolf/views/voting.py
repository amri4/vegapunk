import discord

from ..buttons.vote import VoteButton
from ..game import get_alive_players


class VotingView(discord.ui.View):
    def __init__(self, game_id):
        super().__init__(timeout=None)

        players = get_alive_players(game_id)

        for voter in players:
            if voter[3] != 0:
                continue

            for target in players:
                if target[0] == voter[0]:
                    continue

                label = target[6] or "Player"

                self.add_item(
                    VoteButton(
                        game_id,
                        voter[0],
                        target[0],
                        label[:80]
                    )
                )
