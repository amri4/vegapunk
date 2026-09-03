import mycord

from discord import Member
from discord.ext import commands

from ..functions.get_member_rank import get_member_rank


db = mycord.PunksDB()


@commands.command(
    name="demote",
    help="Demote a member to the next lower staff rank."
)
async def demote(
    ctx,
    member: Member
):

    current_rank = get_member_rank(member)

    if current_rank is None:
        await ctx.send(
            f"❌ {member.mention} doesn't have a staff rank."
        )
        return

    lower_rank = db.fetchone(
        "staff_ranks",
        "guild_id = ? AND level < ?",
        (
            ctx.guild.id,
            current_rank["level"]
        )
    )

    if lower_rank is None:
        await member.remove_roles(
            ctx.guild.get_role(current_rank["role_id"]),
            reason=f"Demoted by {ctx.author}"
        )

        await ctx.send(
            f"⬇️ Removed **{current_rank['name']}** "
            f"from {member.mention}. They had the lowest rank."
        )

        return

    current_role = ctx.guild.get_role(
        current_rank["role_id"]
    )

    lower_role = ctx.guild.get_role(
        lower_rank["role_id"]
    )

    if current_role:
        await member.remove_roles(
            current_role,
            reason=f"Demoted by {ctx.author}"
        )

    if lower_role:
        await member.add_roles(
            lower_role,
            reason=f"Demoted by {ctx.author}"
        )

    await ctx.send(
        f"⬇️ {member.mention} was demoted from "
        f"**{current_rank['name']}** to "
        f"**{lower_rank['name']}**."
    )


def setup(bot):
    bot.add_command(demote)