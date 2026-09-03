import discord
from discord.ext import commands

from ..functions.find_rank import find_rank


@commands.command(
    name="viewpermissions",
    help="Show the current permissions of a staff rank."
)
async def viewpermissions(
    ctx,
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

    enabled = []
    disabled = []

    for name, value in role.permissions:

        name = name.replace("_", " ").title()

        if value:
            enabled.append(name)
        else:
            disabled.append(name)

    embed = discord.Embed(
        title=f"{rank['name']} Permissions",
        description=role.mention
    )

    embed.add_field(
        name="✅ Enabled",
        value="\n".join(
            f"• {permission}"
            for permission in enabled
        ) or "None",
        inline=False
    )

    embed.add_field(
        name="❌ Disabled",
        value="\n".join(
            f"• {permission}"
            for permission in disabled
        ) or "None",
        inline=False
    )

    await ctx.send(embed=embed)


def setup(bot):
    bot.add_command(viewpermissions)