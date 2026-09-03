import mycord


db = mycord.PunksDB()


async def on_guild_role_delete(role):

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