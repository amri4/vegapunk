import discord

from ..buttons.buy import BuyButton
from ..items import SHOP_ITEMS
from ..functions.shop import get_items


class ShopView(discord.ui.View):

    def __init__(
        self,
        item
    ):
        super().__init__(
            timeout=None
        )

        self.add_item(
            BuyButton(item)
        )


def setup(bot):
    saved_items = get_items()

    saved_item_ids = {
        item[0]
        for item in saved_items
    }

    for item in SHOP_ITEMS:
        if item["id"] in saved_item_ids:
            bot.add_view(
                ShopView(item)
            )