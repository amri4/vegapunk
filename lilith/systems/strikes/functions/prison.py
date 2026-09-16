import time

import mycord


db = mycord.DB()


def imprison(guild_id, user_id, duration):

    prison_until = int(time.time()) + duration

    existing = db.fetchone(
        "strikes",
        "guild_id = ? AND user_id = ?",
        (guild_id, user_id)
    )

    if existing is None:

        db.insert(
            "strikes",
            "guild_id, user_id, strikes, prison_until",
            (
                guild_id,
                user_id,
                5,
                prison_until
            )
        )

    else:

        db.update(
            "strikes = ?, prison_until = ?",
            "guild_id = ? AND user_id = ?",
            (
                5,
                prison_until,
                guild_id,
                user_id
            )
        )

    return prison_until


def is_imprisoned(guild_id, user_id):

    existing = db.fetchone(
        "strikes",
        "guild_id = ? AND user_id = ?",
        (guild_id, user_id)
    )

    if existing is None:
        return False

    prison_until = existing[3]

    if prison_until is None:
        return False

    return int(time.time()) < prison_until


def release(guild_id, user_id):

    existing = db.fetchone(
        "strikes",
        "guild_id = ? AND user_id = ?",
        (guild_id, user_id)
    )

    if existing is None:
        return False

    db.delete(
        "strikes",
        "guild_id = ? AND user_id = ?",
        (guild_id, user_id)
    )

    return True