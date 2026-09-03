import mycord


db = mycord.PunksDB()


async def on_guild_role_delete(role):

    # Find the staff rank using this role
    rank = db.fetchone(
        "staff_ranks",
        "guild_id = ? AND role_id = ?",
        (
            role.guild.id,
            role.id
        )
    )

    if rank is None:
        return

    # Remove command requirements using this rank
    db.delete(
        "command_ranks",
        "guild_id = ? AND required_level = ?",
        (
            role.guild.id,
            rank["level"]
        )
    )

    # Remove the staff rank itself
    db.delete(
        "staff_ranks",
        "guild_id = ? AND role_id = ?",
        (
            role.guild.id,
            role.id
        )
    )


def setup(bot):
    bot.add_listener(
        on_guild_role_delete,
        "on_guild_role_delete"
    )