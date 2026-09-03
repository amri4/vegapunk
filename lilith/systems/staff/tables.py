import mycord


db = mycord.PunksDB()


# =========================================
# STAFF RANKS
# =========================================

db.create_table(
    "staff_ranks",
    """
    guild_id INTEGER,
    name TEXT,
    role_id INTEGER,
    level INTEGER,

    PRIMARY KEY (
        guild_id,
        level
    )
    """
)


# =========================================
# COMMAND RANKS
# =========================================

db.create_table(
    "command_ranks",
    """
    guild_id INTEGER,
    command_name TEXT,
    required_level INTEGER,

    PRIMARY KEY (
        guild_id,
        command_name
    )
    """
)