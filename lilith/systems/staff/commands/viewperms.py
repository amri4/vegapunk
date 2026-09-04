import discord
from discord.ext import commands

from ..functions.find_rank import find_rank


@commands.command(
    name="viewperms",
    help="View the permissions of a staff rank."
)
async def viewperms(ctx, *, argument: str):

    rank = find_rank(
        ctx.guild,
        argument
    )

    if rank is None:
        await ctx.send(
            f"❌ Staff rank **{argument}** was not found."
        )
        return

    role = ctx.guild.get_role(rank[2])

    if role is None:
        await ctx.send(
            "❌ The Discord role for this staff rank no longer exists."
        )
        return

    permissions = role.permissions

    enabled = []
    disabled = []

    for name, value in permissions.to_dict().items():

        display_name = name.replace("_", " ").title()

        if value:
            enabled.append(f"✅ {display_name}")
        else:
            disabled.append(f"❌ {display_name}")

    embed = discord.Embed(
        title=f"🔐 {role.name} Permissions",
        description=f"**Level {rank[3]}**"
    )

    embed.add_field(
        name=f"✅ ON ({len(enabled)})",
        value="\n".join(enabled) or "None",
        inline=False
    )

    embed.add_field(
        name=f"❌ OFF ({len(disabled)})",
        value="\n".join(disabled) or "None",
        inline=False
    )

    await ctx.send(embed=embed)


def setup(bot):
    bot.add_command(viewperms)