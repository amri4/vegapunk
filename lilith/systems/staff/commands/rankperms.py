import discord
from discord.ext import commands

from ..functions.find_rank import find_rank


def find_permission(permission_name):

    search = (
        permission_name
        .casefold()
        .replace(" ", "_")
        .replace("-", "_")
    )

    valid_permissions = {
        name
        for name, value
        in discord.Permissions.none()
    }

    if search in valid_permissions:
        return search

    return None


@commands.command(
    name="rankperms",
    help="Change a staff rank's Discord permissions."
)
async def rankperms(ctx, *, arguments: str):

    # =========================================
    # SPLIT ARGUMENTS
    # =========================================

    parts = arguments.rsplit(
        " ",
        2
    )

    if len(parts) != 3:

        await ctx.send(
            "❌ Usage: `rankperms <rank> "
            "<permission> <on/off>`"
        )

        return

    argument, permission_text, state = parts

    # =========================================
    # FIND RANK
    # =========================================

    rank = find_rank(
        ctx.guild,
        argument
    )

    if rank is None:

        await ctx.send(
            f"❌ Staff rank **{argument}** was not found."
        )

        return

    # =========================================
    # FIND ROLE
    # =========================================

    role = ctx.guild.get_role(
        rank[2]
    )

    if role is None:

        await ctx.send(
            "❌ The Discord role for this "
            "staff rank no longer exists."
        )

        return

    # =========================================
    # FIND PERMISSION
    # =========================================

    permission_name = find_permission(
        permission_text
    )

    if permission_name is None:

        await ctx.send(
            f"❌ Unknown permission "
            f"**{permission_text}**."
        )

        return

    # =========================================
    # VALIDATE STATE
    # =========================================

    state = state.casefold()

    if state not in (
        "on",
        "off"
    ):

        await ctx.send(
            "❌ Use `on` or `off`."
        )

        return

    # =========================================
    # CHANGE PERMISSION
    # =========================================

    enabled = state == "on"

    try:

        permissions = role.permissions

        permissions.update(
            **{
                permission_name: enabled
            }
        )

        await role.edit(
            permissions=permissions,
            reason=(
                "Lilith: Staff rank "
                "permission updated."
            )
        )

    except discord.Forbidden:

        await ctx.send(
            "❌ I don't have permission "
            "to edit this role."
        )

        return

    except discord.HTTPException as error:

        await ctx.send(
            f"❌ Discord failed to update "
            f"the permission: `{error}`"
        )

        return

    # =========================================
    # SUCCESS
    # =========================================

    display_name = (
        permission_name
        .replace("_", " ")
        .title()
    )

    status = (
        "enabled"
        if enabled
        else "disabled"
    )

    await ctx.send(
        f"✅ **{display_name}** has been "
        f"**{status}** for {role.mention}."
    )


def setup(bot):
    bot.add_command(rankperms)