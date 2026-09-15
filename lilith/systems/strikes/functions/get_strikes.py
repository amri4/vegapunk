import mycord


db = mycord.DB()


def get_strikes(guild_id, user_id):

    existing = db.fetchone(
        "strikes",
        "guild_id = ? AND user_id = ?",
        (guild_id, user_id)
    )

    if existing is None:
        return 0

    return existing[2]