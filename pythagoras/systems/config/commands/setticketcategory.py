import discord
from discord.ext import commands

import mycord

from ..functions.get_config import get_config


db = mycord.PunksDB()


@commands.command(
    name="setticketcategory",
    help="Set the category where Atlas tickets are created."
)
async def setticketcategory(
    ctx,
    category: discord.CategoryChannel
):

    config = get_config(
        ctx.guild
    )

    try:

        db.update(
            "server_config",
            "ticket_category_id = ?",
            "guild_id = ?",
            (
                category.id,
                ctx.guild.id
            )
        )

    except Exception as error:

        await ctx.send(
            f"❌ Failed to save the ticket category: `{error}`"
        )

        return

    await ctx.send(
        f"✅ Tickets will now be created in **{category.name}**."
    )


def setup(bot):
    bot.add_command(
        setticketcategory
    )