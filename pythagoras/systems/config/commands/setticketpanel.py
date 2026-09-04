import discord
from discord.ext import commands

import mycord

from ..functions.get_config import get_config


db = mycord.PunksDB()


@commands.command(
    name="setticketpanel",
    help="Set the channel where Atlas ticket panels are posted."
)
async def setticketpanel(
    ctx,
    channel: discord.TextChannel
):

    config = get_config(
        ctx.guild
    )

    try:

        db.update(
            "server_config",
            "ticket_panel_channel_id = ?",
            "guild_id = ?",
            (
                channel.id,
                ctx.guild.id
            )
        )

    except Exception as error:

        await ctx.send(
            f"❌ Failed to save the ticket panel channel: `{error}`"
        )

        return

    await ctx.send(
        f"✅ Ticket panels will now be posted in {channel.mention}."
    )


def setup(bot):
    bot.add_command(
        setticketpanel
    )