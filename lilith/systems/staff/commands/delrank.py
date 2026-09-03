import discord
from discord.ext import commands

import mycord

from ..functions.find_rank import find_rank
from ..functions.arrange_roles import arrange_roles


db = mycord.PunksDB()


@commands.command(
    name="delrank",
    help="Delete a staff hierarchy rank."
)
async def delrank(ctx, *, argument: str):

    rank = find_rank(
        ctx.guild,
        argument
    )

    if rank is None:
        await ctx.send(
            "❌ I couldn't find that staff rank."
        )
        return

    role = ctx.guild.get_role(
        rank["role_id"]
    )

    rank_name = rank["name"]

    # Delete the Discord role
    if role is not None:
        await role.delete(
            reason=f"Staff rank deleted by {ctx.author}"
        )

    # Delete the database entry
    db.delete(
        "staff_ranks",
        "guild_id = ? AND level = ?",
        (
            ctx.guild.id,
            rank["level"]
        )
    )

    # Re-arrange remaining staff roles
    await arrange_roles(ctx.guild)

    await ctx.send(
        f"🗑️ Deleted staff rank **{rank_name}**."
    )


def setup(bot):
    bot.add_command(delrank)