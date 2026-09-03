import discord
from discord.ext import commands

import mycord


db = mycord.PunksDB()


@commands.command(
    name="hierarchy",
    help="Show the server's staff hierarchy."
)
async def hierarchy(ctx):

    rows = db.fetchall("staff_ranks")

    ranks = [
        row
        for row in rows
        if row["guild_id"] == ctx.guild.id
    ]

    if not ranks:
        await ctx.send(
            "❌ No staff ranks have been configured."
        )
        return

    ranks.sort(
        key=lambda rank: rank["level"],
        reverse=True
    )

    lines = []

    for rank in ranks:

        role = ctx.guild.get_role(
            rank["role_id"]
        )

        if role is None:
            role_text = f"**{rank['name']}**"
        else:
            role_text = role.mention

        lines.append(
            f"**Level {rank['level']}** — {role_text}"
        )

    embed = discord.Embed(
        title="👑 Staff Hierarchy",
        description="\n".join(lines)
    )

    await ctx.send(embed=embed)


def setup(bot):
    bot.add_command(hierarchy)