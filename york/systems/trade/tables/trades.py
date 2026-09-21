import mycord


db = mycord.DB()


db.create_table(
    "trades",
    """
    trade_id INTEGER PRIMARY KEY AUTOINCREMENT,
    guild_id INTEGER,
    sender_id INTEGER,
    receiver_id INTEGER,
    status TEXT
    """
)