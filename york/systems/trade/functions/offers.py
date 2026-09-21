import mycord


db = mycord.DB()


def add_offer(
    trade_id,
    user_id,
    item_id,
    amount
):
    db.insert_replace(
        "trade_offers",
        "trade_id, user_id, item_id, amount",
        (
            trade_id,
            user_id,
            item_id,
            amount
        )
    )


def get_offer(
    trade_id,
    user_id,
    item_id
):
    return db.fetchone(
        "trade_offers",
        "trade_id = ? AND user_id = ? AND item_id = ?",
        (
            trade_id,
            user_id,
            item_id
        )
    )


def get_offers(
    trade_id
):
    offers = db.fetchall(
        "trade_offers"
    )

    return [
        offer
        for offer in offers
        if offer[0] == trade_id
    ]


def remove_offer(
    trade_id,
    user_id,
    item_id
):
    db.delete(
        "trade_offers",
        "trade_id = ? AND user_id = ? AND item_id = ?",
        (
            trade_id,
            user_id,
            item_id
        )
    )


def remove_offers(
    trade_id
):
    db.delete(
        "trade_offers",
        "trade_id = ?",
        (trade_id,)
    )