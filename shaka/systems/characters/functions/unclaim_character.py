import mycord


db = mycord.DB()


def unclaim_character(guild_id, character_name, user_id):
    existing = db.fetchone(
        "character_claims",
        "guild_id = ? AND character_name = ?",
        (guild_id, character_name)
    )

    if existing is None:
        return False

    claimed_by = existing[2]

    if claimed_by != user_id:
        return False

    db.delete(
        "character_claims",
        "guild_id = ? AND character_name = ?",
        (guild_id, character_name)
    )

    return True