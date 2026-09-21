import discord

from ..buttons.add import AddItemButton


class TradeView(discord.ui.View):
    def __init__(self, trade_id):
        super().__init__(
            timeout=None
        )

        self.trade_id = trade_id

        self.add_item(
            AddItemButton(
                trade_id
            )
        )