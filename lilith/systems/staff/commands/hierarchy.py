import discord
from discord.ext import commands

from ..functions.get_ranks import get_ranks


@commands.command(
    name="hierarchy",
    help="Show the server's staff hierarchy."
)
async def hierarchy(ctx):

    ranks = get_ranks(
        ctx.guild
    )

    if not ranks:

        await ctx.send(
            "❌ No staff ranks have been configured."
        )

        return

    ranks.sort(
        key=lambda rank: rank[3]
    )

    lines = []

    for rank in ranks:

        level = rank[3]
        role_id = rank[2]

        role = ctx.guild.get_role(
            role_id
        )

        if role is None:
            role_text = f"**{rank[1]}**"
        else:
            role_text = role.mention

        lines.append(
            f"**Level {level}** — {role_text}"
        )

    embed = discord.Embed(
        title="👑 Staff Hierarchy",
        description="\n".join(lines)
    )

    await ctx.send(
        embed=embed
    )


def setup(bot):
    bot.add_command(hierarchy)