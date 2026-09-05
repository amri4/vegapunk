from discord.ext import commands

import mycord

from ..functions.find_rank import find_rank


db = mycord.DB()


@commands.command(
    name="commandrank",
    help="Set the required staff rank for a command."
)
async def commandrank(ctx, command_name: str, *, rank_argument: str):

    # =========================================
    # FIND COMMAND
    # =========================================

    command = ctx.bot.get_command(
        command_name
    )

    if command is None:

        await ctx.send(
            f"❌ Command **{command_name}** was not found."
        )

        return

    # =========================================
    # FIND STAFF RANK
    # =========================================

    rank = find_rank(
        ctx.guild,
        rank_argument
    )

    if rank is None:

        await ctx.send(
            f"❌ Staff rank **{rank_argument}** was not found."
        )

        return

    command_name = command.qualified_name.casefold()

    # =========================================
    # REMOVE OLD REQUIREMENT
    # =========================================

    try:

        db.delete(
            "command_ranks",
            "guild_id = ? AND command_name = ?",
            (
                ctx.guild.id,
                command_name
            )
        )

    except Exception:
        pass

    # =========================================
    # SAVE NEW REQUIREMENT
    # =========================================

    try:

        db.insert(
            "command_ranks",
            "guild_id, command_name, required_level",
            (
                ctx.guild.id,
                command_name,
                rank[3]
            )
        )

    except Exception as error:

        await ctx.send(
            f"❌ Failed to save the command rank: `{error}`"
        )

        return

    # =========================================
    # SUCCESS
    # =========================================

    await ctx.send(
        f"✅ **{command.qualified_name}** now requires "
        f"**{rank[1]}** or above."
    )


def setup(bot):

    bot.add_command(
        commandrank
    )