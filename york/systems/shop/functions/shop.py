import mycord


db = mycord.DB()


def add_item(item_id, channel_id, message_id):
    db.insert(
        "shop",
        "item_id, channel_id, message_id",
        (
            item_id,
            channel_id,
            message_id
        )
    )


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


def update_message_id(item_id, message_id):
    db.update(
        "shop",
        "message_id = ?",
        "item_id = ?",
        (message_id, item_id)
    )


def remove_item(item_id):
    db.delete(
        "shop",
        "item_id = ?",
        (item_id,)
    )