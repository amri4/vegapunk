import mycord


db = mycord.DB()


def add_strike(guild_id, user_id):

    existing = db.fetchone(
        "strikes",
        "guild_id = ? AND user_id = ?",
        (guild_id, user_id)
    )

    if existing is None:

        db.insert(
            "strikes",
            "guild_id, user_id, strikes",
            (guild_id, user_id, 1)
        )

        return 1

    new_strikes = existing[2] + 1

    db.update(
        "strikes",
        "strikes = ?",
        "guild_id = ? AND user_id = ?",
        (
            new_strikes,
            guild_id,
            user_id
        )
    )

    return new_strikes