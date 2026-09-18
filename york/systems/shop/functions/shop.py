import mycord


db = mycord.DB()


def add_item(
    title,
    description,
    price,
    channel_id,
    reward_type
):
    db.insert(
        "shop",
        "title, description, price, channel_id, message_id, reward_type",
        (
            title,
            description,
            price,
            channel_id,
            0,
            reward_type
        )
    )

    item = db.fetchone(
        "shop",
        """
        title = ?
        AND description = ?
        AND price = ?
        AND channel_id = ?
        AND message_id = ?
        AND reward_type = ?
        """,
        (
            title,
            description,
            price,
            channel_id,
            0,
            reward_type
        )
    )

    return item[0]


def get_item(item_id):
    return db.fetchone(
        "shop",
        "item_id = ?",
        (item_id,)
    )


def get_items():
    return db.fetchall(
        "shop"
    )


def update_message_id(
    item_id,
    message_id
):
    db.update(
        "shop",
        "message_id = ?",
        "item_id = ?",
        (
            message_id,
            item_id
        )
    )


def remove_item(item_id):
    db.delete(
        "shop",
        "item_id = ?",
        (item_id,)
    )