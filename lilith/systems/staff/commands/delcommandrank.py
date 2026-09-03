import mycord

from discord.ext import commands


db = mycord.PunksDB()


@commands.command(
    name="delcommandrank",
    help="Remove the staff rank requirement from a command."
)
async def delcommandrank(
    ctx,
    command_name: str
):

    command_name = command_name.lower().strip()

    existing = db.fetchone(
        "command_ranks",
        "guild_id = ? AND command_name = ?",
        (
            ctx.guild.id,
            command_name
        )
    )

    if existing is None:
        await ctx.send(
            f"❌ `{command_name}` doesn't have a rank requirement."
        )
        return

    db.delete(
        "command_ranks",
        "guild_id = ? AND command_name = ?",
        (
            ctx.guild.id,
            command_name
        )
    )

    await ctx.send(
        f"✅ Removed the staff rank requirement "
        f"from `{command_name}`."
    )


def setup(bot):
    bot.add_command(delcommandrank)