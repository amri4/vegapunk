import discord

from ..buttons.respond import (
    AcceptTradeButton,
    DeclineTradeButton
)


class TradeRespondView(discord.ui.View):
    def __init__(self, trade_id):
        super().__init__(
            timeout=None
        )

        self.add_item(
            AcceptTradeButton(
                trade_id
            )
        )

        self.add_item(
            DeclineTradeButton(
                trade_id
            )
        )