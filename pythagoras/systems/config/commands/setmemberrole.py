import discord
from discord.ext import commands

from ..functions.get_config import get_config


@commands.command(
    name="setmemberrole",
    help="Set the role given to verified members."
)
async def setmemberrole(
    ctx,
    role: discord.Role
):

    get_config(ctx.guild)

    from ..tables import db

    db.update(
        "server_config",
        "member_role_id = ?",
        "guild_id = ?",
        (
            role.id,
            ctx.guild.id
        )
    )

    await ctx.send(
        f"✅ The member role is now {role.mention}."
    )


def setup(bot):
    bot.add_command(setmemberrole)