import mycord


db = mycord.DB()


def get_fragments(
    guild_id,
    user_id
):
    result = db.fetchone(
        "fragments",
        "guild_id = ? AND user_id = ?",
        (
            guild_id,
            user_id
        )
    )

    if result is None:
        return 0

    return result[2]


def add_fragments(
    guild_id,
    user_id,
    amount
):
    current = get_fragments(
        guild_id,
        user_id
    )

    if current == 0:
        db.insert_replace(
            "fragments",
            "user_id, guild_id, amount",
            (
                user_id,
                guild_id,
                amount
            )
        )

    else:
        db.update(
            "fragments",
            "amount = ?",
            "guild_id = ? AND user_id = ?",
            (
                current + amount,
                guild_id,
                user_id
            )
        )


def remove_fragments(
    guild_id,
    user_id,
    amount
):
    current = get_fragments(
        guild_id,
        user_id
    )

    if current < amount:
        return False

    db.update(
        "fragments",
        "amount = ?",
        "guild_id = ? AND user_id = ?",
        (
            current - amount,
            guild_id,
            user_id
        )
    )

    return True