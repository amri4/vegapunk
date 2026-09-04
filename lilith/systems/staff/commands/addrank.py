import discord
from discord.ext import commands

import mycord

from ..functions.get_ranks import get_ranks
from ..functions.arrange_roles import arrange_roles


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

    name = name.strip()

    if not name:
        await ctx.send(
            "❌ You must provide a rank name."
        )
        return

    # =========================================
    # GET EXISTING RANKS
    # =========================================

    ranks = get_ranks(ctx.guild)

    # Level already exists
    if any(
        rank[3] == level
        for rank in ranks
    ):

        await ctx.send(
            f"❌ **Level {level}** is already in use."
        )

        return

    # =========================================
    # CHECK DUPLICATE NAME
    # =========================================

    normalized_name = " ".join(
        name.casefold().split()
    )

    if any(
        " ".join(
            rank[1].casefold().split()
        ) == normalized_name
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
            name=name,
            reason="Staff rank created."
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
                reason="Failed to save staff rank."
            )
        except Exception:
            pass

        await ctx.send(
            f"❌ Failed to save the staff rank: `{error}`"
        )

        return

    # =========================================
    # ARRANGE STAFF ROLES
    # =========================================

    try:

        arranged = await arrange_roles(
            ctx.guild
        )

    except (discord.Forbidden, discord.HTTPException) as error:

        await ctx.send(
            f"⚠️ Created **Level {level} — {role.mention}**, "
            f"but I couldn't arrange the staff roles: `{error}`"
        )

        return

    if not arranged:

        await ctx.send(
            f"⚠️ Created **Level {level} — {role.mention}**, "
            "but I couldn't determine my role position."
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