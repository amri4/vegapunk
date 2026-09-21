import mycord


db = mycord.DB()


def create_trade(
    guild_id,
    sender_id,
    receiver_id
):
    db.insert(
        "trades",
        "guild_id, sender_id, receiver_id, status",
        (
            guild_id,
            sender_id,
            receiver_id,
            "pending"
        )
    )

    trades = db.fetchall(
        "trades"
    )

    return trades[-1][0]


def get_trade(
    trade_id
):
    return db.fetchone(
        "trades",
        "trade_id = ?",
        (trade_id,)
    )


def update_trade_status(
    trade_id,
    status
):
    db.update(
        "trades",
        "status = ?",
        "trade_id = ?",
        (
            status,
            trade_id
        )
    )


def delete_trade(
    trade_id
):
    db.delete(
        "trades",
        "trade_id = ?",
        (trade_id,)
    )


    def get_trades():
    return db.fetchall("trades")