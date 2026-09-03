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

    ranks = [
        row
        for row in rows
        if row["guild_id"] == ctx.guild.id
    ]

    await ctx.send(
        f"👑 Found **{len(ranks)}** staff ranks in this server."
    )


def setup(bot):
    bot.add_command(hierarchy)