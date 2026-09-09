import mycord


db = mycord.DB()


db.create_table(
    "bounties",
    """
    guild_id INTEGER,
    user_id INTEGER,
    bounty INTEGER DEFAULT 0
    """
)