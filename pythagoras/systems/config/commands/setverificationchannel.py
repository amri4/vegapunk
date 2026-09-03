import discord
from discord.ext import commands

from ..functions.get_config import get_config
from ..tables import db


@commands.command(
    name="setverificationchannel",
    help="Set the channel used for member verification."
)
async def setverificationchannel(
    ctx,
    channel: discord.TextChannel
):

    get_config(ctx.guild)

    db.update(
        "server_config",
        "verification_channel_id = ?",
        "guild_id = ?",
        (
            channel.id,
            ctx.guild.id
        )
    )

    await ctx.send(
        f"✅ The verification channel is now {channel.mention}."
    )


def setup(bot):
    bot.add_command(setverificationchannel)