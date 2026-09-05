import mycord


db = mycord.DB()


def get_config(guild):

    if guild is None:
        return None

    config = db.fetchone(
        "server_config",
        "guild_id = ?",
        (guild.id,)
    )

    if config is None:

        db.insert(
            "server_config",
            "guild_id",
            (guild.id,)
        )

        config = db.fetchone(
            "server_config",
            "guild_id = ?",
            (guild.id,)
        )

    return config