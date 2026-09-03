import discord
from discord.ext import commands

from ..functions.find_rank import find_rank


@commands.command(
    name="rankpermissions",
    help="Change the Discord permissions of a staff rank."
)
async def rankpermissions(
    ctx,
    rank_name: str,
    permission: str,
    value: str
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

    permission = permission.lower().strip()
    value = value.lower().strip()

    valid_values = {
        "on": True,
        "true": True,
        "yes": True,
        "enable": True,
        "enabled": True,

        "off": False,
        "false": False,
        "no": False,
        "disable": False,
        "disabled": False
    }

    if value not in valid_values:
        await ctx.send(
            "❌ Use `on` or `off` for the permission value."
        )
        return

    if permission not in discord.Permissions.VALID_FLAGS:
        await ctx.send(
            f"❌ `{permission}` isn't a valid Discord permission."
        )
        return

    permissions = role.permissions

    setattr(
        permissions,
        permission,
        valid_values[value]
    )

    await role.edit(
        permissions=permissions,
        reason=f"Rank permissions changed by {ctx.author}"
    )

    status = "enabled" if valid_values[value] else "disabled"

    await ctx.send(
        f"✅ **{rank['name']}**: "
        f"`{permission}` {status}."
    )


def setup(bot):
    bot.add_command(rankpermissions)