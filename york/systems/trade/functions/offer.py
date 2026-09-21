from ...inventory.functions.inventory import get_amount
from .offers import add_offer


def add_item_to_trade(
    trade_id,
    guild_id,
    user_id,
    item_id,
    amount
):
    current = get_amount(
        guild_id,
        user_id,
        item_id
    )

    if current < amount:
        return False

    add_offer(
        trade_id,
        user_id,
        item_id,
        amount
    )

    return True