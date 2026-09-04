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

    # =====================================
    # MEMBER ROLE
    # =====================================

    member_role_id = data[1]

    member_role = (
        ctx.guild.get_role(
            member_role_id
        )
        if member_role_id
        else None
    )

    # =====================================
    # VERIFICATION CHANNEL
    # =====================================

    verification_channel_id = data[2]

    verification_channel = (
        ctx.guild.get_channel(
            verification_channel_id
        )
        if verification_channel_id
        else None
    )

    # =====================================
    # VERIFICATION
    # =====================================

    verification_enabled = data[3]

    # =====================================
    # TICKET PANEL CHANNEL
    # =====================================

    ticket_panel_channel_id = data[4]

    ticket_panel_channel = (
        ctx.guild.get_channel(
            ticket_panel_channel_id
        )
        if ticket_panel_channel_id
        else None
    )

    # =====================================
    # TICKET CATEGORY
    # =====================================

    ticket_category_id = data[5]

    ticket_category = (
        ctx.guild.get_channel(
            ticket_category_id
        )
        if ticket_category_id
        else None
    )

    # =====================================
    # EMBED
    # =====================================

    embed = discord.Embed(
        title="⚙️ Server Configuration",
        description=(
            f"Configuration for **{ctx.guild.name}**"
        ),
        color=discord.Color.blue()
    )

    # =====================================
    # MEMBER ROLE
    # =====================================

    embed.add_field(
        name="👤 Member Role",
        value=(
            member_role.mention
            if member_role
            else "❌ Not configured"
        ),
        inline=True
    )

    # =====================================
    # VERIFICATION CHANNEL
    # =====================================

    embed.add_field(
        name="✅ Verification Channel",
        value=(
            verification_channel.mention
            if verification_channel
            else "❌ Not configured"
        ),
        inline=True
    )

    # =====================================
    # VERIFICATION
    # =====================================

    embed.add_field(
        name="🔐 Verification",
        value=(
            "✅ Enabled"
            if verification_enabled
            else "❌ Disabled"
        ),
        inline=True
    )

    # =====================================
    # TICKET PANEL CHANNEL
    # =====================================

    embed.add_field(
        name="🎫 Ticket Panel Channel",
        value=(
            ticket_panel_channel.mention
            if ticket_panel_channel
            else "❌ Not configured"
        ),
        inline=True
    )

    # =====================================
    # TICKET CATEGORY
    # =====================================

    embed.add_field(
        name="📁 Ticket Category",
        value=(
            ticket_category.name
            if ticket_category
            else "❌ Not configured"
        ),
        inline=True
    )

    # =====================================
    # FOOTER
    # =====================================

    embed.set_footer(
        text="Pythagoras • Server Configuration"
    )

    await ctx.send(
        embed=embed
    )


def setup(bot):
    bot.add_command(config)