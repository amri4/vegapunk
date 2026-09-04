import mycord


db = mycord.PunksDB()


db.create_table(
    "server_config",
    """
    guild_id INTEGER PRIMARY KEY,

    member_role_id INTEGER,

    verification_channel_id INTEGER,
    verification_enabled INTEGER,

    ticket_panel_channel_id INTEGER,
    ticket_category_id INTEGER
    """
)