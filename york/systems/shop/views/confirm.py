import discord

from ..functions.shop import get_item
from ..buttons.confirm import ConfirmButton
from ..buttons.cancel import CancelButton


class ConfirmView(discord.ui.View):

    def __init__(
        self,
        item_id,
        user_id
    ):
        super().__init__(
            timeout=60
        )

        self.item_id = item_id
        self.user_id = user_id

        self.add_item(
            ConfirmButton(
                item_id,
                user_id
            )
        )

        self.add_item(
            CancelButton(
                user_id
            )
        )


def confirmation_embed(item):
    title = item[1]
    description = item[2]
    price = item[3]

    return discord.Embed(
        title="🛒 Confirm Purchase",
        description=(
            f"**{title}**\n\n"
            f"{description}\n\n"
            f"**Price:** {price:,} 🍓\n\n"
            "Are you sure you want to buy this?"
        )
    )