import mycord


db = mycord.DB()


db.create_table(
    "shop",
    """
    item_id TEXT,
    guild_id INTEGER,
    channel_id INTEGER,
    message_id INTEGER,
    PRIMARY KEY (item_id, guild_id)
    """
)