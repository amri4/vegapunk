import mycord


db = mycord.DB()


def confirm_trade(
    trade_id,
    user_id
):
    db.insert_replace(
        "trade_confirmations",
        "trade_id, user_id",
        (
            trade_id,
            user_id
        )
    )


def is_confirmed(
    trade_id,
    user_id
):
    return db.exists(
        "trade_confirmations",
        "trade_id = ? AND user_id = ?",
        (
            trade_id,
            user_id
        )
    )


def get_confirmations(
    trade_id
):
    confirmations = db.fetchall(
        "trade_confirmations"
    )

    return [
        confirmation
        for confirmation in confirmations
        if confirmation[0] == trade_id
    ]


def clear_confirmations(
    trade_id
):
    db.delete(
        "trade_confirmations",
        "trade_id = ?",
        (trade_id,)
    )