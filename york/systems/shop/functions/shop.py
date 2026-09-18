import mycord


db = mycord.DB()


def add_item(
    title,
    description,
    price,
    channel_id,
    message_id
):
    db.insert(
        "shop",
        "title, description, price, channel_id, message_id",
        (
            title,
            description,
            price,
            channel_id,
            message_id
        )
    )


def get_item(
    item_id
):
    return db.fetchone(
        "shop",
        "item_id = ?",
        (item_id,)
    )


def get_items():
    return db.fetchall(
        "shop"
    )


def remove_item(
    item_id
):
    db.delete(
        "shop",
        "item_id = ?",
        (item_id,)
    )