from discord.ext import commands

import mycord

from ..functions.find_rank import find_rank
from ..functions.arrange_roles import arrange_roles


db = mycord.PunksDB()


@commands.command(
    name="moverank",
    help="Change a staff rank's hierarchy level."
)
async def moverank(
    ctx,
    rank_name: str,
    new_level: int
):

    if new_level < 1:
        await ctx.send(
            "❌ Rank level must be 1 or higher."
        )
        return

    rank = find_rank(
        ctx.guild,
        rank_name
    )

    if rank is None:
        await ctx.send(
            "❌ I couldn't find that staff rank."
        )
        return

    if rank["level"] == new_level:
        await ctx.send(
            "❌ That rank is already at that level."
        )
        return

    existing = db.fetchone(
        "staff_ranks",
        "guild_id = ? AND level = ?",
        (
            ctx.guild.id,
            new_level
        )
    )

    if existing:
        await ctx.send(
            "❌ That rank level is already occupied."
        )
        return

    db.update(
        "staff_ranks",
        "level = ?",
        "guild_id = ? AND level = ?",
        (
            new_level,
            ctx.guild.id,
            rank["level"]
        )
    )

    await arrange_roles(ctx.guild)

    await ctx.send(
        f"✅ **{rank['name']}** is now "
        f"**Level {new_level}**."
    )


def setup(bot):
    bot.add_command(moverank)