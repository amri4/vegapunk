import mycord


db = mycord.PunksDB()


db.create_table(
    "server_config",
    """
    guild_id INTEGER PRIMARY KEY,
    member_role_id INTEGER,
    verification_channel_id INTEGER,
    unverified_role_id INTEGER,
    welcome_channel_id INTEGER
    """
)