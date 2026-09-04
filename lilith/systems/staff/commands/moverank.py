from discord.ext import commands

import mycord

from ..functions.find_rank import find_rank
from ..functions.get_ranks import get_ranks
from ..functions.arrange_roles import arrange_roles


db = mycord.PunksDB()


@commands.command(
    name="moverank",
    help="Move a staff rank to another level."
)
async def moverank(ctx, new_level: int, *, argument: str):

    # =========================================
    # VALIDATE LEVEL
    # =========================================

    if new_level < 1:

        await ctx.send(
            "❌ The rank level must be 1 or higher."
        )

        return

    # =========================================
    # FIND RANK
    # =========================================

    rank = find_rank(
        ctx.guild,
        argument
    )

    if rank is None:

        await ctx.send(
            f"❌ Staff rank **{argument}** was not found."
        )

        return

    guild_id = rank[0]
    old_level = rank[3]

    # =========================================
    # ALREADY THERE
    # =========================================

    if old_level == new_level:

        await ctx.send(
            f"❌ **{rank[1]}** is already Level {new_level}."
        )

        return

    # =========================================
    # GET ALL RANKS
    # =========================================

    ranks = get_ranks(
        ctx.guild
    )

    # =========================================
    # MOVING UP
    # =========================================

    if new_level < old_level:

        affected = [
            other
            for other in ranks
            if new_level <= other[3] < old_level
        ]

        affected.sort(
            key=lambda other: other[3],
            reverse=True
        )

        try:

            for other in affected:

                db.update(
                    "staff_ranks",
                    "level = ?",
                    "guild_id = ? AND level = ?",
                    (
                        other[3] + 1,
                        guild_id,
                        other[3]
                    )
                )

            db.update(
                "staff_ranks",
                "level = ?",
                "guild_id = ? AND level = ?",
                (
                    new_level,
                    guild_id,
                    old_level
                )
            )

        except Exception as error:

            await ctx.send(
                f"❌ Failed to move the rank: `{error}`"
            )

            return

    # =========================================
    # MOVING DOWN
    # =========================================

    else:

        affected = [
            other
            for other in ranks
            if old_level < other[3] <= new_level
        ]

        affected.sort(
            key=lambda other: other[3]
        )

        try:

            for other in affected:

                db.update(
                    "staff_ranks",
                    "level = ?",
                    "guild_id = ? AND level = ?",
                    (
                        other[3] - 1,
                        guild_id,
                        other[3]
                    )
                )

            db.update(
                "staff_ranks",
                "level = ?",
                "guild_id = ? AND level = ?",
                (
                    new_level,
                    guild_id,
                    old_level
                )
            )

        except Exception as error:

            await ctx.send(
                f"❌ Failed to move the rank: `{error}`"
            )

            return

    # =========================================
    # ARRANGE DISCORD ROLES
    # =========================================

    try:

        await arrange_roles(
            ctx.guild
        )

    except Exception as error:

        await ctx.send(
            f"⚠️ The rank was moved in PunksDB, "
            f"but the Discord roles could not be rearranged: `{error}`"
        )

        return

    # =========================================
    # SUCCESS
    # =========================================

    await ctx.send(
        f"✅ Moved **{rank[1]}** "
        f"from Level {old_level} to Level {new_level}."
    )


def setup(bot):
    bot.add_command(moverank)