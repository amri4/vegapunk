import discord
from discord.ext import commands

from ..functions.get_config import get_config


@commands.command(
    name="config",
    help="Show this server's configuration."
)
async def config(ctx):

    data = get_config(ctx.guild)

    if not data:
        await ctx.send(
            "❌ Couldn't load the server configuration."
        )
        return

    embed = discord.Embed(
        title="⚙️ Server Configuration",
        description=f"Configuration for **{ctx.guild.name}**",
        color=discord.Color.blue()
    )

    # Member Role
    member_role = None

    if len(data) > 1 and data[1]:
        member_role = ctx.guild.get_role(data[1])

    embed.add_field(
        name="👤 Member Role",
        value=(
            member_role.mention
            if member_role
            else "❌ Not configured"
        ),
        inline=True
    )

    # Verification Channel
    verification_channel = None

    if len(data) > 2 and data[2]:
        verification_channel = ctx.guild.get_channel(data[2])

    embed.add_field(
        name="✅ Verification Channel",
        value=(
            verification_channel.mention
            if verification_channel
            else "❌ Not configured"
        ),
        inline=True
    )

    # Verification
    verification_enabled = (
        bool(data[3])
        if len(data) > 3 and data[3] is not None
        else False
    )

    embed.add_field(
        name="🔐 Verification",
        value=(
            "✅ Enabled"
            if verification_enabled
            else "❌ Disabled"
        ),
        inline=True
    )

    # Ticket Panel Channel
    ticket_panel_channel = None

    if len(data) > 4 and data[4]:
        ticket_panel_channel = ctx.guild.get_channel(data[4])

    embed.add_field(
        name="🎫 Ticket Panel Channel",
        value=(
            ticket_panel_channel.mention
            if ticket_panel_channel
            else "❌ Not configured"
        ),
        inline=True
    )

    embed.set_footer(
        text="Pythagoras • Server Configuration"
    )

    await ctx.send(embed=embed)


def setup(bot):
    bot.add_command(config)