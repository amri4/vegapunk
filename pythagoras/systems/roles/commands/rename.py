from discord.ext import commands

from ..functions.find_role import find_role


@commands.command(
    name="editrole",
    help="Rename an existing server role."
)
async def editrole(
    ctx,
    role: str,
    *,
    name: str
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
            "❌ I can't edit @everyone."
        )
        return

    if role >= ctx.guild.me.top_role:
        await ctx.send(
            "❌ I can't edit that role because "
            "it's higher than or equal to my "
            "highest role."
        )
        return

    name = name.strip()

    if not name:
        await ctx.send(
            "❌ Please provide a new role name."
        )
        return

    old_name = role.name

    await role.edit(
        name=name,
        reason=f"Edited by {ctx.author}"
    )

    await ctx.send(
        f"✏️ Renamed **{old_name}** → "
        f"{role.mention}."
    )


def setup(bot):
    bot.add_command(editrole)