from ...berries.functions.berries import get_berries
from .offers import add_offer


BERRIES_ITEM_ID = "berries"


def add_berries_to_trade(
    trade_id,
    guild_id,
    user_id,
    amount
):
    current = get_berries(
        guild_id,
        user_id
    )

    if current < amount:
        return False

    add_offer(
        trade_id,
        user_id,
        BERRIES_ITEM_ID,
        amount
    )

    return True