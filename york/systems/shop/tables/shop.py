import mycord


db = mycord.DB()


db.create_table(
    "shop",
    """
    item_id TEXT PRIMARY KEY,
    channel_id INTEGER NOT NULL,
    message_id INTEGER NOT NULL
    """
)