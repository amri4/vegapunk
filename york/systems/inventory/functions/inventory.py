import mycord


db = mycord.DB()


def get_item(
    guild_id,
    user_id,
    item_id
):
    return db.fetchone(
        "inventory",
        "guild_id = ? AND user_id = ? AND item_id = ?",
        (
            guild_id,
            user_id,
            item_id
        )
    )


def get_amount(
    guild_id,
    user_id,
    item_id
):
    result = get_item(
        guild_id,
        user_id,
        item_id
    )

    if result is None:
        return 0

    return result[3]


def add_item(
    guild_id,
    user_id,
    item_id,
    amount=1
):
    current = get_amount(
        guild_id,
        user_id,
        item_id
    )

    if current == 0:
        db.insert_replace(
            "inventory",
            "user_id, guild_id, item_id, amount",
            (
                user_id,
                guild_id,
                item_id,
                amount
            )
        )
        return

    db.update(
        "inventory",
        "amount = ?",
        "guild_id = ? AND user_id = ? AND item_id = ?",
        (
            current + amount,
            guild_id,
            user_id,
            item_id
        )
    )


def remove_item(
    guild_id,
    user_id,
    item_id,
    amount=1
):
    current = get_amount(
        guild_id,
        user_id,
        item_id
    )

    if current < amount:
        return False

    new_amount = current - amount

    if new_amount == 0:
        db.delete(
            "inventory",
            "guild_id = ? AND user_id = ? AND item_id = ?",
            (
                guild_id,
                user_id,
                item_id
            )
        )
        return True

    db.update(
        "inventory",
        "amount = ?",
        "guild_id = ? AND user_id = ? AND item_id = ?",
        (
            new_amount,
            guild_id,
            user_id,
            item_id
        )
    )

    return True


def get_inventory(
    guild_id,
    user_id
):
    items = db.fetchall(
        "inventory"
    )

    return [
        item
        for item in items
        if item[0] == user_id
        and item[1] == guild_id
    ]