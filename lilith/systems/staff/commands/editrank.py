from discord.ext import commands

from ..functions.find_rank import find_rank
from ..functions.arrange_roles import arrange_roles


@commands.command(
    name="editrank",
    help="Change the name of a staff hierarchy rank."
)
async def editrank(
    ctx,
    rank_name: str,
    *,
    new_name: str
):

    rank = find_rank(
        ctx.guild,
        rank_name
    )

    if rank is None:
        await ctx.send(
            "❌ I couldn't find that staff rank."
        )
        return

    new_name = new_name.strip()

    if not new_name:
        await ctx.send(
            "❌ Please provide a new rank name."
        )
        return

    role = ctx.guild.get_role(
        rank["role_id"]
    )

    if role is None:
        await ctx.send(
            "❌ The Discord role for that rank no longer exists."
        )
        return

    await role.edit(
        name=new_name,
        reason=f"Staff rank renamed by {ctx.author}"
    )

    from ..tables import db

    db.update(
        "staff_ranks",
        "name = ?",
        "guild_id = ? AND level = ?",
        (
            new_name,
            ctx.guild.id,
            rank["level"]
        )
    )

    await arrange_roles(ctx.guild)

    await ctx.send(
        f"✅ Renamed the staff rank to **{new_name}**."
    )


def setup(bot):
    bot.add_command(editrank)