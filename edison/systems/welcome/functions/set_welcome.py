import mycord


db = mycord.DB()


def set_welcome(guild_id, channel_id):
    existing = db.fetchone(
        "welcome",
        "guild_id = ?",
        (guild_id,)
    )

    if existing is None:
        db.insert(
            "welcome",
            "guild_id, channel_id",
            (guild_id, channel_id)
        )
    else:
        db.update(
            "welcome",
            "channel_id = ?",
            "guild_id = ?",
            (channel_id, guild_id)
        )