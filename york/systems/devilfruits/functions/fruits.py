import mycord


db = mycord.DB()


def add_fruit(
    fruit_id,
    name,
    emoji,
    rarity,
    tradeable=True,
    sell_value=0
):
    db.insert_replace(
        "devil_fruits",
        "id, name, emoji, rarity, tradeable, sell_value",
        (
            fruit_id,
            name,
            emoji,
            rarity,
            int(tradeable),
            sell_value
        )
    )


def get_fruit(fruit_id):
    return db.fetchone(
        "devil_fruits",
        "id = ?",
        (fruit_id,)
    )


def get_fruits():
    return db.fetchall(
        "devil_fruits"
    )


def update_fruit(
    fruit_id,
    set_values,
    values
):
    db.update(
        "devil_fruits",
        set_values,
        "id = ?",
        (
            *values,
            fruit_id
        )
    )


def remove_fruit(fruit_id):
    db.delete(
        "devil_fruits",
        "id = ?",
        (fruit_id,)
    )