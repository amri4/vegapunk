import mycord


db = mycord.DB()


def set_bounty(
    guild_id,
    user_id,
    amount
):
    if db.exists(
        "bounties",
        "guild_id = ? AND user_id = ?",
        (guild_id, user_id)
    ):
        db.update(
            "bounties",
            "bounty = ?",
            "guild_id = ? AND user_id = ?",
            (amount, guild_id, user_id)
        )

    else:
        db.insert(
            "bounties",
            "guild_id, user_id, bounty",
            (guild_id, user_id, amount)
        )