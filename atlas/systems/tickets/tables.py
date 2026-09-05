import mycord


db = mycord.DB()


# =========================================
# TICKET PANELS
# =========================================

db.create_table(
    "ticket_panels",
    """
    panel_id INTEGER PRIMARY KEY AUTOINCREMENT,

    guild_id INTEGER,
    message_id INTEGER,

    title TEXT,
    description TEXT,

    image_url TEXT,
    thumbnail_url TEXT
    """
)


# =========================================
# TICKET TYPES
# =========================================

db.create_table(
    "ticket_types",
    """
    ticket_type_id INTEGER PRIMARY KEY AUTOINCREMENT,

    guild_id INTEGER,
    panel_id INTEGER,

    name TEXT,
    color TEXT,

    ticket_message TEXT,
    message_image_url TEXT
    """
)


# =========================================
# TICKETS
# =========================================

db.create_table(
    "tickets",
    """
    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,

    guild_id INTEGER,

    panel_id INTEGER,
    ticket_type_id INTEGER,

    channel_id INTEGER,
    member_id INTEGER,

    status TEXT
    """
)