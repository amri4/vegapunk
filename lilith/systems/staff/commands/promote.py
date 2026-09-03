import discord
from discord.ext import commands

from ..functions.find_rank import find_rank
from ..functions.get_member_rank import get_member_rank


@commands.command(
    name="promote",
    help="Give a member a staff hierarchy rank."
)
async def promote(
    ctx,
    member: discord.Member,
    *,
    rank_name: str
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

    role = ctx.guild.get_role(
        rank["role_id"]
    )

    if role is None:
        await ctx.send(
            "❌ The Discord role for that rank no longer exists."
        )
        return

    current_rank = get_member_rank(member)

    # Already has this rank
    if current_rank and current_rank["level"] == rank["level"]:
        await ctx.send(
            f"❌ {member.mention} already has "
            f"the **{rank['name']}** rank."
        )
        return

    # Remove their current staff rank
    if current_rank:

        current_role = ctx.guild.get_role(
            current_rank["role_id"]
        )

        if current_role:
            await member.remove_roles(
                current_role,
                reason=f"Promoted by {ctx.author}"
            )

    # Give the new rank
    await member.add_roles(
        role,
        reason=f"Promoted by {ctx.author}"
    )

    await ctx.send(
        f"⬆️ {member.mention} is now "
        f"**{rank['name']}** (Level {rank['level']})."
    )


def setup(bot):
    bot.add_command(promote)