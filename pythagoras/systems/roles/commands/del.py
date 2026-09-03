from discord.ext import commands

from ..functions.find_role import find_role


@commands.command(
    name="delrole",
    help="Delete a server role."
)
async def delrole(ctx, *, name: str):

    result = find_role(
        ctx.guild,
        name
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
            "❌ I can't delete @everyone."
        )
        return

    if role >= ctx.guild.me.top_role:
        await ctx.send(
            "❌ I can't delete that role because "
            "it's higher than or equal to my "
            "highest role."
        )
        return

    role_name = role.name

    await role.delete(
        reason=f"Deleted by {ctx.author}"
    )

    await ctx.send(
        f"🗑️ Deleted role **{role_name}**."
    )


def setup(bot):
    bot.add_command(delrole)