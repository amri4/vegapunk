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
    round INTEGER NOT NULL DEFAULT 0,
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

db.create_table(
    "werewolf_actions",
    """
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER NOT NULL,
    round INTEGER NOT NULL,
    phase TEXT NOT NULL,
    player_id INTEGER NOT NULL,
    action TEXT NOT NULL,
    target_id INTEGER
    """
)

db.create_table(
    "werewolf_votes",
    """
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER NOT NULL,
    round INTEGER NOT NULL,
    voter_id INTEGER NOT NULL,
    target_id INTEGER NOT NULL
    """
)
