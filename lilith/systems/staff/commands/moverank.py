from discord.ext import commands

import mycord

from ..functions.find_rank import find_rank
from ..functions.get_ranks import get_ranks
from ..functions.arrange_roles import arrange_roles


db = mycord.DB()


@commands.command(
    name="moverank",
    help="Move a staff rank to another level."
)
async def moverank(ctx, *, arguments: str):

    parts = arguments.rsplit(" ", 1)

    if len(parts) != 2:

        await ctx.send(
            "❌ Usage: `lilith moverank <rank> <level>`"
        )

        return

    argument, level_text = parts

    try:
        new_level = int(level_text)

    except ValueError:

        await ctx.send(
            "❌ The new level must be a number."
        )

        return

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
    rank_name = rank[1]
    old_level = rank[3]

    # =========================================
    # ALREADY AT LEVEL
    # =========================================

    if old_level == new_level:

        await ctx.send(
            f"❌ **{rank_name}** is already Level {new_level}."
        )

        return

    # =========================================
    # GET ALL RANKS
    # =========================================

    ranks = get_ranks(
        ctx.guild
    )

    max_level = max(
        other[3]
        for other in ranks
    )

    if new_level > max_level:

        await ctx.send(
            f"❌ Level {new_level} does not exist."
        )

        return

    # =========================================
    # CALCULATE FINAL LEVELS
    # =========================================

    final_levels = {}

    for other in ranks:

        other_role_id = other[2]
        other_level = other[3]

        if other_role_id == rank[2]:

            final_levels[other_role_id] = new_level

        elif new_level < old_level:

            if new_level <= other_level < old_level:
                final_levels[other_role_id] = other_level + 1

            else:
                final_levels[other_role_id] = other_level

        else:

            if old_level < other_level <= new_level:
                final_levels[other_role_id] = other_level - 1

            else:
                final_levels[other_role_id] = other_level

    # =========================================
    # MOVE EVERYTHING TO TEMPORARY LEVELS
    # =========================================

    try:

        for index, other in enumerate(ranks):

            temporary_level = -(index + 1)

            db.update(
                "staff_ranks",
                "level = ?",
                "guild_id = ? AND level = ?",
                (
                    temporary_level,
                    guild_id,
                    other[3]
                )
            )

    except Exception as error:

        await ctx.send(
            f"❌ Failed to prepare the rank move: `{error}`"
        )

        return

    # =========================================
    # APPLY FINAL LEVELS
    # =========================================

    try:

        for index, other in enumerate(ranks):

            temporary_level = -(index + 1)
            final_level = final_levels[other[2]]

            db.update(
                "staff_ranks",
                "level = ?",
                "guild_id = ? AND level = ?",
                (
                    final_level,
                    guild_id,
                    temporary_level
                )
            )

    except Exception as error:

        await ctx.send(
            f"❌ Failed to finish moving the rank: `{error}`"
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
        f"✅ Moved **{rank_name}** "
        f"from Level {old_level} to Level {new_level}."
    )


def setup(bot):
    bot.add_command(moverank)