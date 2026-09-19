import mycord


db = mycord.DB()


def set_shop_channel(guild_id, channel_id):
    db.insert_replace(
        "shop",
        "item_id, guild_id, channel_id, message_id",
        (
            "__channel__",
            guild_id,
            channel_id,
            0
        )
    )


def get_shop_channel(guild_id):
    result = db.fetchone(
        "shop",
        "item_id = ? AND guild_id = ?",
        (
            "__channel__",
            guild_id
        )
    )

    if result is None:
        return None

    return result[2]


def add_item(
    item_id,
    guild_id,
    channel_id,
    message_id
):
    db.insert(
        "shop",
        "item_id, guild_id, channel_id, message_id",
        (
            item_id,
            guild_id,
            channel_id,
            message_id
        )
    )


def get_item(item_id, guild_id):
    return db.fetchone(
        "shop",
        "item_id = ? AND guild_id = ?",
        (
            item_id,
            guild_id
        )
    )


def get_items(guild_id):
    items = db.fetchall(
        "shop"
    )

    return [
        item
        for item in items
        if item[1] == guild_id
    ]


def update_message_id(
    item_id,
    guild_id,
    message_id
):
    db.update(
        "shop",
        "message_id = ?",
        "item_id = ? AND guild_id = ?",
        (
            message_id,
            item_id,
            guild_id
        )
    )


def remove_item(
    item_id,
    guild_id
):
    db.delete(
        "shop",
        "item_id = ? AND guild_id = ?",
        (
            item_id,
            guild_id
        )
    )

Now "/syncshop" should get past that DB error.