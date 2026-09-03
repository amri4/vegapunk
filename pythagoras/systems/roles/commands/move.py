from discord.ext import commands

from ..functions.find_role import find_role


@commands.command(
    name="moverole",
    help="Move a role above or below another role."
)
async def moverole(
    ctx,
    role: str,
    position: str,
    target: str
):

    result = find_role(
        ctx.guild,
        role
    )

    if result is None:
        await ctx.send(
            "❌ I couldn't find the role to move."
        )
        return

    if isinstance(result, list):
        names = "\n".join(
            f"• {item.mention}"
            for item in result[:10]
        )

        await ctx.send(
            "❌ Multiple roles found:\n"
            + names
        )
        return

    role = result

    result = find_role(
        ctx.guild,
        target
    )

    if result is None:
        await ctx.send(
            "❌ I couldn't find the target role."
        )
        return

    if isinstance(result, list):
        names = "\n".join(
            f"• {item.mention}"
            for item in result[:10]
        )

        await ctx.send(
            "❌ Multiple target roles found:\n"
            + names
        )
        return

    target = result

    position = position.lower()

    if position not in ("above", "below"):
        await ctx.send(
            "❌ Position must be `above` or `below`."
        )
        return

    if role == ctx.guild.default_role:
        await ctx.send(
            "❌ I can't move @everyone."
        )
        return

    if target == ctx.guild.default_role:
        await ctx.send(
            "❌ You can't move a role relative to @everyone."
        )
        return

    if role == target:
        await ctx.send(
            "❌ The two roles must be different."
        )
        return

    bot_role = ctx.guild.me.top_role

    if role >= bot_role:
        await ctx.send(
            "❌ I can't move that role because "
            "it's higher than or equal to my highest role."
        )
        return

    if target >= bot_role:
        await ctx.send(
            "❌ I can't move a role relative to "
            "a role that's higher than or equal "
            "to my highest role."
        )
        return

    if position == "above":
        new_position = target.position + 1
    else:
        new_position = target.position - 1

    new_position = max(
        1,
        min(
            new_position,
            bot_role.position - 1
        )
    )

    await role.edit(
        position=new_position,
        reason=f"Moved by {ctx.author}"
    )

    await ctx.send(
        f"↕️ Moved {role.mention} "
        f"**{position}** {target.mention}."
    )


def setup(bot):
    bot.add_command(moverole)