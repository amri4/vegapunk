import discord
from discord.ext import commands

import mycord

from ..functions.arrange_roles import arrange_roles


db = mycord.PunksDB()


@commands.command(
    name="addrank",
    help="Create a new staff hierarchy rank."
)
async def addrank(ctx, level: int, *, name: str):

    name = name.strip()

    if not name:
        await ctx.send(
            "❌ Please provide a rank name."
        )
        return

    if level < 1:
        await ctx.send(
            "❌ Rank level must be 1 or higher."
        )
        return

    existing = db.fetchone(
        "staff_ranks",
        "guild_id = ? AND level = ?",
        (
            ctx.guild.id,
            level
        )
    )

    if existing:
        await ctx.send(
            "❌ That rank level already exists."
        )
        return

    role = await ctx.guild.create_role(
        name=name,
        reason=f"Staff rank created by {ctx.author}"
    )

    db.insert(
        "staff_ranks",
        """
        guild_id,
        name,
        role_id,
        level
        """,
        (
            ctx.guild.id,
            name,
            role.id,
            level
        )
    )

    await arrange_roles(ctx.guild)

    await ctx.send(
        f"✅ Created staff rank {role.mention} "
        f"at level **{level}**."
    )


def setup(bot):
    bot.add_command(addrank)