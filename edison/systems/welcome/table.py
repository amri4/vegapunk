import mycord


db = mycord.DB()


db.create_table(
    "welcome",
    """
    guild_id INTEGER PRIMARY KEY,
    channel_id INTEGER NOT NULL
    """
)