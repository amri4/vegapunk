import discord
from discord.ext import commands

from ..functions.find_rank import find_rank


@commands.command(
    name="rankinfo",
    help="Show information about a staff hierarchy rank."
)
async def rankinfo(
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

    permissions = [
        name.replace("_", " ").title()
        for name, value in role.permissions
        if value
    ]

    embed = discord.Embed(
        title=f"👑 {rank['name']}",
        description=role.mention
    )

    embed.add_field(
        name="Level",
        value=str(rank["level"]),
        inline=True
    )

    embed.add_field(
        name="Members",
        value=str(len(role.members)),
        inline=True
    )

    embed.add_field(
        name="Enabled Permissions",
        value="\n".join(
            f"• {permission}"
            for permission in permissions
        ) or "None",
        inline=False
    )

    await ctx.send(embed=embed)


def setup(bot):
    bot.add_command(rankinfo)