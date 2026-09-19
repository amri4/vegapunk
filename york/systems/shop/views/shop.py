import discord

from ..buttons.buy import BuyButton
from ..items import SHOP_ITEMS


class ShopView(discord.ui.View):
    def __init__(self, item):
        super().__init__(timeout=None)

        self.add_item(
            BuyButton(item)
        )


def setup(bot):
    for item in SHOP_ITEMS:
        bot.add_view(
            ShopView(item)
        )