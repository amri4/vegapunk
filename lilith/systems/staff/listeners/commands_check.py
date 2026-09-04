from discord.ext import commands

from ..functions.check_command_rank import check_command_rank
from ..functions.get_command_rank import get_command_rank


async def check_command(ctx):

    # Don't apply staff ranks in DMs
    if ctx.guild is None:
        return

    # Ignore the help command itself
    if ctx.command is None:
        return

    required_rank = get_command_rank(
        ctx.guild,
        ctx.command.name
    )

    # No requirement configured
    if required_rank is None:
        return

    if check_command_rank(
        ctx.author,
        ctx.command.name
    ):
        return

    await ctx.send(
        f"❌ You need **{required_rank[1]}** "
        "or above to use this command."
    )

    raise commands.CheckFailure(
        "Insufficient staff rank."
    )


def setup(bot):

    bot.before_invoke(
        check_command
    )