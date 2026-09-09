import discord
import mycord

from ..buttons.night import NightActionButton
from ..game import get_game, get_alive_players

db = mycord.DB()


class NightView(discord.ui.View):
    def __init__(self, game_id):
        super().__init__(timeout=None)

        game = get_game(game_id)

        if game is None:
            return

        for player in get_alive_players(game_id):
            if player[3] != 0:
                continue

            if player[4] not in ("werewolf", "seer", "doctor"):
                continue

            for target in get_alive_players(game_id):
                if target[0] == player[0]:
                    continue

                if player[4] == "werewolf" and target[4] == "werewolf":
                    continue

                label = target[6] or "Player"

                self.add_item(
                    NightActionButton(
                        game_id,
                        player[0],
                        target[0],
                        label[:80]
                    )
                )
