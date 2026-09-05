import discord
from discord.ext import commands

import mycord

from ..functions.find_rank import find_rank
from ..functions.get_ranks import get_ranks


db = mycord.DB()


@commands.command(
    name="delrank",
    help="Delete a staff rank."
)
async def delrank(ctx, *, argument: str):

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
    role_id = rank[2]
    level = rank[3]

    # =========================================
    # FIND ROLE
    # =========================================

    role = ctx.guild.get_role(
        role_id
    )

    # =========================================
    # CHECK MEMBERS
    # =========================================

    if role is not None:

        members = [
            member
            for member in ctx.guild.members
            if role in member.roles
        ]

        if members:

            await ctx.send(
                f"❌ Cannot delete **{rank_name}** "
                f"because {len(members)} member(s) "
                "currently have this staff rank."
            )

            return

    # =========================================
    # DELETE DATABASE ENTRY
    # =========================================

    try:

        db.delete(
            "staff_ranks",
            "guild_id = ? AND level = ?",
            (
                guild_id,
                level
            )
        )

    except Exception as error:

        await ctx.send(
            f"❌ Failed to delete the staff rank: `{error}`"
        )

        return

    # =========================================
    # CLOSE LEVEL GAP
    # =========================================

    ranks = get_ranks(
        ctx.guild
    )

    lower_ranks = [
        rank
        for rank in ranks
        if rank[3] > level
    ]

    lower_ranks.sort(
        key=lambda rank: rank[3],
        reverse=True
    )

    try:

        for rank in lower_ranks:

            db.update(
                "staff_ranks",
                "level = ?",
                "guild_id = ? AND level = ?",
                (
                    rank[3] - 1,
                    guild_id,
                    rank[3]
                )
            )

    except Exception as error:

        await ctx.send(
            f"⚠️ The rank was deleted, but the hierarchy "
            f"could not be completely reorganized: `{error}`"
        )

        return

    # =========================================
    # DELETE DISCORD ROLE
    # =========================================

    if role is not None:

        try:

            await role.delete(
                reason="Staff rank deleted."
            )

        except discord.Forbidden:

            await ctx.send(
                f"⚠️ Deleted **{rank_name}** from PunksDB, "
                "but I don't have permission to delete the Discord role."
            )

            return

        except discord.HTTPException as error:

            await ctx.send(
                f"⚠️ Deleted **{rank_name}** from PunksDB, "
                f"but Discord failed to delete the role: `{error}`"
            )

            return

    # =========================================
    # SUCCESS
    # =========================================

    await ctx.send(
        f"✅ Deleted **Level {level} — {rank_name}**."
    )


def setup(bot):
    bot.add_command(delrank)