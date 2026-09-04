import discord
from discord.ext import commands

from ..functions.find_rank import find_rank


@commands.command(
    name="viewperms",
    help="View the permissions of a staff rank."
)
async def viewperms(ctx, *, argument: str):

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
    # FIND DISCORD ROLE
    # =========================================

    role = ctx.guild.get_role(
        rank[2]
    )

    if role is None:

        await ctx.send(
            "❌ The Discord role for this staff rank "
            "no longer exists."
        )

        return

    # =========================================
    # GET PERMISSIONS
    # =========================================

    enabled = []
    disabled = []

    for permission_name, value in role.permissions:

        display_name = (
            permission_name
            .replace("_", " ")
            .title()
        )

        if value:

            enabled.append(
                f"✅ {display_name}"
            )

        else:

            disabled.append(
                f"❌ {display_name}"
            )

    # =========================================
    # CREATE EMBED
    # =========================================

    embed = discord.Embed(
        title=f"🔐 {role.name} Permissions",
        description=(
            f"**Staff Level:** {rank[3]}"
        )
    )

    # Discord embed fields have a 1024-character limit,
    # so split permissions into multiple fields.

    def add_permission_fields(
        title,
        permissions_list
    ):

        if not permissions_list:

            embed.add_field(
                name=title,
                value="None",
                inline=False
            )

            return

        current = ""

        for permission in permissions_list:

            line = f"{permission}\n"

            if len(current) + len(line) > 1000:

                embed.add_field(
                    name=title,
                    value=current,
                    inline=False
                )

                current = ""

            current += line

        if current:

            embed.add_field(
                name=title,
                value=current,
                inline=False
            )

    # =========================================
    # ADD ENABLED PERMISSIONS
    # =========================================

    add_permission_fields(
        f"✅ Enabled ({len(enabled)})",
        enabled
    )

    # =========================================
    # ADD DISABLED PERMISSIONS
    # =========================================

    add_permission_fields(
        f"❌ Disabled ({len(disabled)})",
        disabled
    )

    # =========================================
    # SEND
    # =========================================

    await ctx.send(
        embed=embed
    )


def setup(bot):
    bot.add_command(viewperms)