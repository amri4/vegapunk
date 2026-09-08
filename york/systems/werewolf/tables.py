import mycord

db = mycord.DB()

db.create_table(
    "werewolf_games",
    """
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guild_id INTEGER NOT NULL,
    channel_id INTEGER NOT NULL,
    creator_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'lobby',
    phase TEXT,
    werewolves INTEGER NOT NULL,
    seers INTEGER NOT NULL,
    doctors INTEGER NOT NULL
    """
)

db.create_table(
    "werewolf_players",
    """
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER NOT NULL,
    user_id INTEGER,
    is_bot INTEGER NOT NULL DEFAULT 0,
    role TEXT,
    alive INTEGER NOT NULL DEFAULT 1,
    display_name TEXT
    """
)