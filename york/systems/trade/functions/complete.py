from ...inventory.functions.inventory import (
    add_item,
    remove_item
)

from ...berries.functions.berries import (
    add_berries,
    remove_berries
)

from .offers import get_offers
from .validate import validate_trade


BERRIES_ITEM_ID = "berries"


def complete_trade(
    trade
):
    trade_id = trade[0]
    guild_id = trade[1]
    sender_id = trade[2]
    receiver_id = trade[3]

    offers = get_offers(
        trade_id
    )

    if not validate_trade(
        trade,
        offers
    ):
        return False

    for offer in offers:
        user_id = offer[1]
        item_id = offer[2]
        amount = offer[3]

        if item_id == BERRIES_ITEM_ID:
            remove_berries(
                guild_id,
                user_id,
                amount
            )
        else:
            remove_item(
                guild_id,
                user_id,
                item_id,
                amount
            )

    for offer in offers:
        user_id = offer[1]
        item_id = offer[2]
        amount = offer[3]

        if user_id == sender_id:
            receiver = receiver_id
        else:
            receiver = sender_id

        if item_id == BERRIES_ITEM_ID:
            add_berries(
                guild_id,
                receiver,
                amount
            )
        else:
            add_item(
                guild_id,
                receiver,
                item_id,
                amount
            )

    return True