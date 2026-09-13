# table.py

import mycord


db = mycord.DB()


db.create_table(
    "character_claims",
    """
    guild_id INTEGER NOT NULL,
    character_name TEXT NOT NULL,
    claimed_by INTEGER NOT NULL,
    claimed_at INTEGER NOT NULL,
    PRIMARY KEY (guild_id, character_name)
    """
)


db.create_table(
    "character_panels",
    """
    guild_id INTEGER PRIMARY KEY,
    channel_id INTEGER NOT NULL,
    message_id INTEGER NOT NULL
    """
)