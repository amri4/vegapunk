import discord
from discord.ext import commands

from ..functions.get_config import get_config


@commands.command(
    name="config",
    help="Show this server's configuration."
)
async def config(ctx):

    data = get_config(
        ctx.guild
    )

    if not data:
        await ctx.send(
            "❌ Couldn't load the server configuration."
        )
        return

    member_role_id = data[1]

    role = (
        ctx.guild.get_role(member_role_id)
        if member_role_id
        else None
    )

    embed = discord.Embed(
        title="⚙️ Server Configuration",
        description=f"Configuration for **{ctx.guild.name}**"
    )

    embed.add_field(
        name="👤 Member Role",
        value=(
            role.mention
            if role
            else "Not configured"
        ),
        inline=True
    )

    await ctx.send(
        embed=embed
    )


def setup(bot):
    bot.add_command(config)