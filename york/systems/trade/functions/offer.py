from ...inventory.functions.inventory import get_amount

from ...devilfruits.functions.fruits import get_fruit

from .offers import (
    add_offer,
    get_offer,
    remove_offer,
    update_offer
)

from .confirmations import clear_confirmations


BERRIES_ITEM_ID = "berries"


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

    fruit = get_fruit(
        item_id
    )

    if fruit is not None:
        tradeable = fruit[4]

        if not tradeable:
            return False

    add_offer(
        trade_id,
        user_id,
        item_id,
        amount
    )

    clear_confirmations(
        trade_id
    )

    return True


def remove_item_from_trade(
    trade_id,
    user_id,
    item_id,
    amount
):
    offer = get_offer(
        trade_id,
        user_id,
        item_id
    )

    if offer is None:
        return False

    current = offer[3]

    if amount > current:
        return False

    if amount == current:
        remove_offer(
            trade_id,
            user_id,
            item_id
        )

    else:
        update_offer(
            trade_id,
            user_id,
            item_id,
            current - amount
        )

    clear_confirmations(
        trade_id
    )

    return True