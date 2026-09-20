import mycord


db = mycord.DB()


db.create_table(
    "inventory",
    """
    user_id INTEGER,
    guild_id INTEGER,
    item_id TEXT,
    amount INTEGER DEFAULT 0,
    PRIMARY KEY (user_id, guild_id, item_id)
    """
)