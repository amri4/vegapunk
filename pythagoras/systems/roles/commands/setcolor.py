import discord
from discord.ext import commands

from ..functions.find_role import find_role
from utils.role_colors import parse_role_color


@commands.command(
    name="setrolecolor",
    help="Change the color of a server role."
)
async def setrolecolor(
    ctx,
    role: str,
    color: str
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
            f"• {item.mention}"
            for item in result[:10]
        )

        await ctx.send(
            "❌ Multiple roles found:\n"
            + names
        )
        return

    role = result

    if role == ctx.guild.default_role:
        await ctx.send(
            "❌ I can't change the color of @everyone."
        )
        return

    if role >= ctx.guild.me.top_role:
        await ctx.send(
            "❌ I can't change that role because "
            "it's higher than or equal to my "
            "highest role."
        )
        return

    parsed_color = parse_role_color(color)

    if parsed_color is None:
        await ctx.send(
            "❌ Invalid color.\n\n"
            "Use a color name such as "
            "`red`, `crimson`, `cyan`, "
            "`gold`, `lavender`, etc.\n\n"
            "Or use a hex code such as "
            "`#5865F2`."
        )
        return

    await role.edit(
        color=discord.Color(parsed_color),
        reason=f"Color changed by {ctx.author}"
    )

    await ctx.send(
        f"🎨 Changed {role.mention} to `{color}`."
    )


def setup(bot):
    bot.add_command(setrolecolor)