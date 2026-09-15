import mycord

db = mycord.DB()

db.create_table(
    "strikes",
    """
    guild_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    strikes INTEGER NOT NULL DEFAULT 0,
    prison_until INTEGER,
    PRIMARY KEY (guild_id, user_id)
    """
)