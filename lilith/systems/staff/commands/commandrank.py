from discord.ext import commands

import mycord

from ..functions.find_rank import find_rank


db = mycord.PunksDB()


@commands.command(
    name="commandrank",
    help="Set the minimum staff rank required for a command."
)
async def commandrank(
    ctx,
    command_name: str,
    *,
    rank_name: str
):

    command_name = command_name.lower().strip()

    rank = find_rank(
        ctx.guild,
        rank_name
    )

    if rank is None:
        await ctx.send(
            "❌ I couldn't find that staff rank."
        )
        return

    db.insert_replace(
        "command_ranks",
        """
        guild_id,
        command_name,
        required_level
        """,
        (
            ctx.guild.id,
            command_name,
            rank["level"]
        )
    )

    await ctx.send(
        f"✅ `{command_name}` now requires "
        f"**{rank['name']}** (Level {rank['level']})."
    )


def setup(bot):
    bot.add_command(commandrank)