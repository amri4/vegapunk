import discord

from ..buttons.add import AddItemButton
from ..buttons.remove import RemoveItemButton
from ..buttons.confirm import ConfirmTradeButton
from ..buttons.cancel import CancelTradeButton


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

        self.add_item(
            RemoveItemButton(
                trade_id
            )
        )

        self.add_item(
            ConfirmTradeButton(
                trade_id
            )
        )

        self.add_item(
            CancelTradeButton(
                trade_id
            )
        )