import mycord

db = mycord.DB()

MARINE_RANKS = [
    "Chore-Boy",      # 0 (Ex-Pirates who defect)
    "Trainee",        # 1
    "Recruit",        # 2 (Default for new Marines)
    "Lieutenant",     # 3
    "Captain",        # 4
    "Vice Admiral",   # 5 (Max auto-promotion rank)
    "Admiral",        # 6 (Appointed by Fleet Admiral / Admin)
    "Fleet Admiral",  # 7 (Appointed by Admin)
]

HONOR_THRESHOLDS = {
    1: 500,     # Trainee
    2: 1500,    # Recruit
    3: 5000,    # Lieutenant
    4: 15000,   # Captain
    5: 40000,   # Vice Admiral
}


def add_honor(guild_id: int, user_id: int, amount: int):
    """Add Honor from raids/PvP/adventures. Returns new rank name if auto-promoted, else None."""
    row = db.fetchone("marines", "guild_id = ? AND user_id = ?", (guild_id, user_id))
    if row is None:
        rank, honor = 2, 0
        db.insert("marines", "guild_id, user_id, rank, honor", (guild_id, user_id, rank, honor))
    else:
        rank, honor = row[2], row[3]

    new_honor = max(0, honor + amount)
    new_rank = rank

    for target_rank, req_honor in HONOR_THRESHOLDS.items():
        if target_rank > new_rank and new_honor >= req_honor:
            new_rank = target_rank

    db.update(
        "marines",
        "rank = ?, honor = ?",
        "guild_id = ? AND user_id = ?",
        (new_rank, new_honor, guild_id, user_id)
    )

    if new_rank > rank:
        return MARINE_RANKS[new_rank]
    return None