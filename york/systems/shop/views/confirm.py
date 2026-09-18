import discord

from ..buttons.confirm import ConfirmButton
from ..buttons.cancel import CancelButton


class ConfirmView(discord.ui.View):

    def __init__(self, item, user_id):
        super().__init__(
            timeout=60
        )

        self.item = item
        self.user_id = user_id

        self.add_item(
            ConfirmButton(
                item,
                user_id
            )
        )

        self.add_item(
            CancelButton(
                user_id
            )
        )


def confirmation_embed(item):
    return discord.Embed(
        title="🛒 Confirm Purchase",
        description=(
            f"**{item['title']}**\n\n"
            f"{item['description']}\n\n"
            f"**Price:** {item['price']:,} <:berries:1550458400800776344>\n\n"
            "Are you sure you want to buy this?"
        )
    )