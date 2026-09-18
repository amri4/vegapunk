import discord

from ..buttons.buy import BuyButton
from ..functions.shop import get_items


class ShopView(discord.ui.View):
    def __init__(
        self,
        item_id
    ):
        super().__init__(
            timeout=None
        )

        self.add_item(
            BuyButton(item_id)
        )


def setup_shop_views(
    bot
):
    for item in get_items():
        item_id = item[0]

        bot.add_view(
            ShopView(item_id)
        )