import time

import mycord


db = mycord.DB()


def claim_character(guild_id, character_name, user_id):
    existing_character = db.fetchone(
        "character_claims",
        "guild_id = ? AND claimed_by = ?",
        (guild_id, user_id)
    )

    if existing_character is not None:
        return False

    existing_claim = db.fetchone(
        "character_claims",
        "guild_id = ? AND character_name = ?",
        (guild_id, character_name)
    )

    if existing_claim is not None:
        return False

    db.insert(
        "character_claims",
        "guild_id, character_name, claimed_by, claimed_at",
        (
            guild_id,
            character_name,
            user_id,
            int(time.time())
        )
    )

    return True