import mycord


db = mycord.DB()


def unclaim_character(guild_id, user_id):
    existing = db.fetchone(
        "character_claims",
        "guild_id = ? AND claimed_by = ?",
        (guild_id, user_id)
    )

    if existing is None:
        return None

    character_name = existing[1]

    db.delete(
        "character_claims",
        "guild_id = ? AND claimed_by = ?",
        (guild_id, user_id)
    )

    return character_name