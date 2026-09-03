import discord
from discord.ext import commands

from ..functions.get_member_rank import get_member_rank
from ..functions.find_rank import find_rank


@commands.command(
    name="demote",
    help="Remove a member's staff hierarchy rank."
)
async def demote(
    ctx,
    member: discord.Member
):

    current_rank = get_member_rank(member)

    if current_rank is None:
        await ctx.send(
            f"❌ {member.mention} doesn't have a staff rank."
        )
        return

    role = ctx.guild.get_role(
        current_rank["role_id"]
    )

    if role is not None:
        await member.remove_roles(
            role,
            reason=f"Demoted by {ctx.author}"
        )

    await ctx.send(
        f"⬇️ Removed **{current_rank['name']}** "
        f"from {member.mention}."
    )


def setup(bot):
    bot.add_command(demote)