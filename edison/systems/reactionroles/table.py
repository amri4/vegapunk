import mycord

db = mycord.DB()

db.create_table(
    "reaction_roles",
    """
    guild_id INTEGER NOT NULL,
    message_id INTEGER NOT NULL,
    emoji TEXT NOT NULL,
    role_id INTEGER NOT NULL,
    PRIMARY KEY (message_id, emoji)
    """
)