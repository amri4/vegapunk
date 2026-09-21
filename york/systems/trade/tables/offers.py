import mycord


db = mycord.DB()


db.create_table(
    "trade_offers",
    """
    trade_id INTEGER,
    user_id INTEGER,
    item_id TEXT,
    amount INTEGER,
    PRIMARY KEY (trade_id, user_id, item_id)
    """
)