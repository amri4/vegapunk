from discord.ext import commands

from ..functions.find_role import find_role


@commands.command(
    name="takerole",
    help="Remove a role from a member."
)
async def takerole(
    ctx,
    member: commands.MemberConverter,
    role: str
):

    result = find_role(
        ctx.guild,
        role
    )

    if result is None:
        await ctx.send(
            "❌ I couldn't find that role."
        )
        return

    if isinstance(result, list):

        names = "\n".join(
            f"• {role.mention}"
            for role in result[:10]
        )

        await ctx.send(
            "❌ Multiple roles found:\n"
            + names
        )
        return

    role = result

    if role == ctx.guild.default_role:
        await ctx.send(
            "❌ I can't remove @everyone."
        )
        return

    if role >= ctx.guild.me.top_role:
        await ctx.send(
            "❌ I can't remove that role because "
            "it's higher than or equal to my "
            "highest role."
        )
        return

    if role not in member.roles:
        await ctx.send(
            f"❌ {member.mention} doesn't have "
            f"{role.mention}."
        )
        return

    await member.remove_roles(
        role,
        reason=f"Role removed by {ctx.author}"
    )

    await ctx.send(
        f"✅ Removed {role.mention} from "
        f"{member.mention}."
    )


def setup(bot):
    bot.add_command(takerole)