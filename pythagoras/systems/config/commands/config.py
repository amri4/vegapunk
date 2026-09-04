import discord
from discord.ext import commands

from ..get_config import get_config


@commands.command(
    name="config",
    help="View the server configuration."
)
async def config(ctx):

    settings = get_config(ctx.guild)

    if settings is None:
        await ctx.send(
            "❌ Could not load the server configuration."
        )
        return

    member_role_id = settings[1]
    verification_channel_id = settings[2]
    verification_enabled = settings[3]
    ticket_panel_channel_id = settings[4]
    ticket_category_id = settings[5]

    member_role = (
        ctx.guild.get_role(member_role_id)
        if member_role_id
        else None
    )

    verification_channel = (
        ctx.guild.get_channel(verification_channel_id)
        if verification_channel_id
        else None
    )

    ticket_panel_channel = (
        ctx.guild.get_channel(ticket_panel_channel_id)
        if ticket_panel_channel_id
        else None
    )

    ticket_category = (
        ctx.guild.get_channel(ticket_category_id)
        if ticket_category_id
        else None
    )

    embed = discord.Embed(
        title="⚙️ Server Configuration"
    )

    embed.add_field(
        name="👤 Member Role",
        value=(
            member_role.mention
            if member_role
            else "❌ Not set"
        ),
        inline=False
    )

    embed.add_field(
        name="✅ Verification Channel",
        value=(
            verification_channel.mention
            if verification_channel
            else "❌ Not set"
        ),
        inline=False
    )

    embed.add_field(
        name="🔐 Verification",
        value=(
            "✅ Enabled"
            if verification_enabled
            else "❌ Disabled"
        ),
        inline=False
    )

    embed.add_field(
        name="🎫 Ticket Panel Channel",
        value=(
            ticket_panel_channel.mention
            if ticket_panel_channel
            else "❌ Not set"
        ),
        inline=False
    )

    embed.add_field(
        name="📁 Ticket Category",
        value=(
            f"{ticket_category.name}"
            if ticket_category
            else "❌ Not set"
        ),
        inline=False
    )

    await ctx.send(
        embed=embed
    )


def setup(bot):
    bot.add_command(config)