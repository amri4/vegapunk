import mycord


db = mycord.PunksDB()


def get_command_rank(guild, command_name):

    if guild is None:
        return None

    if not command_name:
        return None

    command_name = command_name.lower().strip()

    return db.fetchone(
        "command_ranks",
        "guild_id = ? AND command_name = ?",
        (
            guild.id,
            command_name
        )
    )