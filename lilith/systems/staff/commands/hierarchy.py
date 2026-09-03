from discord.ext import commands


@commands.command(
    name="hierarchy",
    help="Show the server's staff hierarchy."
)
async def hierarchy(ctx):

    await ctx.send(
        "👑 Hierarchy command is working."
    )


def setup(bot):
    bot.add_command(hierarchy)