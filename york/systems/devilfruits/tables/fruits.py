import mycord


db = mycord.DB()


db.create_table(
    "devil_fruits",
    """
    id TEXT PRIMARY KEY,
    name TEXT,
    emoji TEXT,
    rarity TEXT,
    tradeable INTEGER DEFAULT 1,
    sell_value INTEGER DEFAULT 0
    """
)