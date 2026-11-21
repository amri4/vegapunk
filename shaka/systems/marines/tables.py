import mycord

db = mycord.DB()

db.create_table(
    "marines",
    """
    guild_id INTEGER,
    user_id INTEGER,
    rank INTEGER DEFAULT 2,
    honor INTEGER DEFAULT 0
    """
)