import mycord


db = mycord.DB()


def get_bounty(
    guild_id,
    user_id
):
    result = db.fetchone(
        "bounties",
        "guild_id = ? AND user_id = ?",
        (guild_id, user_id)
    )

    if result is None:
        return 0

    return result[2]