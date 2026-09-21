import mycord


db = mycord.DB()


db.create_table(
    "trade_confirmations",
    """
    trade_id INTEGER,
    user_id INTEGER,
    PRIMARY KEY (trade_id, user_id)
    """
)