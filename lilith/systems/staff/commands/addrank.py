import discord
from discord.ext import commands

import mycord

from ..functions.get_ranks import get_ranks


db = mycord.PunksDB()


@commands.command(
    name="addrank",
    help="Create a new staff rank."
)
async def addrank(ctx, level: int, *, name: str):

    # =========================================
    # VALIDATE LEVEL
    # =========================================

    if level < 1:
        await ctx.send(
            "❌ The rank level must be 1 or higher."
        )
        return

    if not name.strip():
        await ctx.send(
            "❌ You must provide a rank name."
        )
        return

    name = name.strip()

    # =========================================
    # GET EXISTING RANKS
    # =========================================

    ranks = get_ranks(ctx.guild)

    # Level already exists
    if any(rank[3] == level for rank in ranks):

        await ctx.send(
            f"❌ **Level {level}** is already in use."
        )
        return

    # Rank name already exists
    name_normalized = " ".join(
        name.casefold().split()
    )

    if any(
        " ".join(rank[1].casefold().split())
        == name_normalized
        for rank in ranks
    ):

        await ctx.send(
            f"❌ A staff rank named **{name}** already exists."
        )
        return

    # =========================================
    # CREATE DISCORD ROLE
    # =========================================

    try:

        role = await ctx.guild.create_role(
            name=name
        )

    except discord.Forbidden:

        await ctx.send(
            "❌ I don't have permission to create roles."
        )
        return

    except discord.HTTPException as error:

        await ctx.send(
            f"❌ Discord failed to create the role: `{error}`"
        )
        return

    # =========================================
    # SAVE TO PUNKSDB
    # =========================================

    try:

        db.insert(
            "staff_ranks",
            "guild_id, name, role_id, level",
            (
                ctx.guild.id,
                name,
                role.id,
                level
            )
        )

    except Exception as error:

        try:
            await role.delete(
                reason="Failed to save staff rank to PunksDB."
            )
        except Exception:
            pass

        await ctx.send(
            f"❌ Failed to save the staff rank: `{error}`"
        )
        return

    # =========================================
    # SUCCESS
    # =========================================

    await ctx.send(
        f"✅ Created **Level {level} — {role.mention}**."
    )


def setup(bot):
    bot.add_command(addrank)