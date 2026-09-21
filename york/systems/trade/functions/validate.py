from ...inventory.functions.inventory import get_amount
from ...berries.functions.berries import get_berries
from ...devilfruits.functions.fruits import get_fruit

from .offers import get_offers


BERRIES_ITEM_ID = "berries"


def validate_trade(
    trade,
    offers
):
    if not offers:
        return False

    guild_id = trade[1]

    for offer in offers:

        user_id = offer[1]
        item_id = offer[2]
        amount = offer[3]

        if item_id == BERRIES_ITEM_ID:

            current = get_berries(
                guild_id,
                user_id
            )

        else:

            current = get_amount(
                guild_id,
                user_id,
                item_id
            )

            fruit = get_fruit(
                item_id
            )

            if fruit is not None:

                tradeable = fruit[4]

                if not tradeable:
                    return False

        if current < amount:
            return False

    return True