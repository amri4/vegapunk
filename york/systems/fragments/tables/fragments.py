import mycord


db = mycord.DB()


db.create_table(
    "fragments",
    """
    user_id INTEGER,
    guild_id INTEGER,
    amount INTEGER DEFAULT 0,
    PRIMARY KEY (user_id, guild_id)
    """
)