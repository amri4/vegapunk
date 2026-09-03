from ..functions.check_command_rank import check_command_rank
from ..functions.get_command_rank import get_command_rank
from discord.ext import commands


async def check_command(ctx):

    if ctx.guild is None:
        return

    required = get_command_rank(
        ctx.guild,
        ctx.command.name
    )

    if required is None:
        return

    if check_command_rank(
        ctx.author,
        ctx.command.name
    ):
        return

    await ctx.send(
        f"❌ You need **{required['name']}** "
        f"or above to use this command."
    )

    raise commands.CheckFailure(
        "Insufficient staff rank."
    )


def setup(bot):
    bot.before_invoke(check_command)