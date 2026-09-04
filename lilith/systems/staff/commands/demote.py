import discord
from discord.ext import commands

from ..functions.get_member_rank import get_member_rank
from ..functions.get_ranks import get_ranks


@commands.command(
    name="demote",
    help="Demote a staff member."
)
async def demote(ctx, member: discord.Member):

    current_rank = get_member_rank(member)

    if current_rank is None:
        await ctx.send(
            f"❌ {member.mention} does not have a staff rank."
        )
        return

    current_level = current_rank[3]

    ranks = get_ranks(ctx.guild)

    lowest_level = max(
        rank[3]
        for rank in ranks
    )

    if current_level == lowest_level:
        await ctx.send(
            f"❌ {member.mention} is already the lowest rank."
        )
        return

    new_rank = next(
        (
            rank
            for rank in ranks
            if rank[3] == current_level + 1
        ),
        None
    )

    if new_rank is None:
        await ctx.send(
            "❌ The next lower staff rank could not be found."
        )
        return

    current_role = ctx.guild.get_role(current_rank[2])
    new_role = ctx.guild.get_role(new_rank[2])

    if new_role is None:
        await ctx.send(
            "❌ The next staff rank role no longer exists."
        )
        return

    try:

        if current_role is not None:
            await member.remove_roles(
                current_role,
                reason="Lilith: Staff demotion."
            )

        await member.add_roles(
            new_role,
            reason="Lilith: Staff demotion."
        )

    except discord.Forbidden:
        await ctx.send(
            "❌ I don't have permission to manage this member's roles."
        )
        return

    except discord.HTTPException as error:
        await ctx.send(
            f"❌ Discord failed to change the staff rank: `{error}`"
        )
        return

    await ctx.send(
        f"⬇️ Demoted {member.mention} to **{new_rank[1]}**."
    )


def setup(bot):
    bot.add_command(demote)