import discord
from discord.ext import commands

from ..functions.find_rank import find_rank


def find_permission(name):

    search = name.casefold().replace(" ", "_")

    for permission, value in discord.Permissions.all().to_dict().items():

        if permission.casefold() == search:
            return permission

    return None


@commands.command(
    name="rankperms",
    help="Change a staff rank's Discord permissions."
)
async def rankperms(
    ctx,
    argument: str,
    permission: str,
    state: str
):

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

    permission_name = find_permission(permission)

    if permission_name is None:
        await ctx.send(
            f"❌ Unknown permission **{permission}**."
        )
        return

    state = state.casefold()

    if state not in ("on", "off"):
        await ctx.send(
            "❌ State must be `on` or `off`."
        )
        return

    permissions = role.permissions

    setattr(
        permissions,
        permission_name,
        state == "on"
    )

    try:

        await role.edit(
            permissions=permissions,
            reason="Lilith: Staff rank permissions updated."
        )

    except discord.Forbidden:
        await ctx.send(
            "❌ I don't have permission to edit this role."
        )
        return

    except discord.HTTPException as error:
        await ctx.send(
            f"❌ Discord failed to update the permissions: `{error}`"
        )
        return

    status = "enabled" if state == "on" else "disabled"

    await ctx.send(
        f"✅ **{permission_name.replace('_', ' ').title()}** "
        f"has been **{status}** for {role.mention}."
    )


def setup(bot):
    bot.add_command(rankperms)