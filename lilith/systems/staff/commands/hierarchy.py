import discord
from discord.ext import commands

import mycord


db = mycord.PunksDB()


@commands.command(
    name="hierarchy",
    help="Show the server's staff hierarchy."
)
async def hierarchy(ctx):

    rows = db.fetchall(
        "staff_ranks"
    )

    # =====================================
    # FILTER THIS SERVER
    # =====================================

    ranks = [
        row
        for row in rows
        if row[0] == ctx.guild.id
    ]

    if not ranks:

        await ctx.send(
            "❌ No staff ranks have been configured."
        )

        return

    # =====================================
    # SORT BY LEVEL
    # LEVEL 1 = HIGHEST
    # =====================================

    ranks.sort(
        key=lambda rank: rank[3]
    )

    lines = []

    # =====================================
    # BUILD HIERARCHY
    # =====================================

    for rank in ranks:

        rank_name = rank[1]
        role_id = rank[2]
        level = rank[3]

        role = ctx.guild.get_role(
            role_id
        )

        if role is not None:

            role_text = role.mention

        else:

            role_text = f"**{rank_name}**"

        lines.append(
            f"**Level {level}** — {role_text}"
        )

    # =====================================
    # EMBED
    # =====================================

    embed = discord.Embed(
        title="👑 Staff Hierarchy",
        description="\n".join(lines)
    )

    await ctx.send(
        embed=embed
    )


def setup(bot):
    bot.add_command(hierarchy)