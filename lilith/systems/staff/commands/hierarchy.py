import mycord
from discord.ext import commands


db = mycord.PunksDB()


@commands.command(
    name="hierarchy",
    help="Show the server's staff hierarchy."
)
async def hierarchy(ctx):

    rows = db.fetchall(
        "staff_ranks"
    )

    await ctx.send(
        f"Guild ID: {rows[0]['guild_id']}"
    )


def setup(bot):
    bot.add_command(hierarchy)