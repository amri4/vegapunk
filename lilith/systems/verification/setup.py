import mycord


db = mycord.DB()


db.create_table(
    "verification_config",
    """
    guild_id INTEGER PRIMARY KEY,
    verified_role_id INTEGER,
    verification_channel_id INTEGER,
    enabled INTEGER NOT NULL DEFAULT 0
    """
)