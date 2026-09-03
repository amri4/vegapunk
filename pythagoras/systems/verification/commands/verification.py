import discord
from discord.ext import commands

from ...config.functions.get_config import get_config
from ...config.tables import db
from ..views.verification_view import create_verification_view


@commands.command(
    name="verification",
    help="Enable or disable member verification."
)
async def verification(
    ctx,
    state: str
):

    state = state.lower().strip()

    if state not in ("on", "off"):
        await ctx.send(
            "❌ Use `on` or `off`."
        )
        return

    config = get_config(ctx.guild)

    if state == "on":

        member_role_id = config["member_role_id"]
        channel_id = config["verification_channel_id"]

        if not member_role_id:
            await ctx.send(
                "❌ Set the member role first."
            )
            return

        if not channel_id:
            await ctx.send(
                "❌ Set the verification channel first."
            )
            return

        member_role = ctx.guild.get_role(
            member_role_id
        )

        channel = ctx.guild.get_channel(
            channel_id
        )

        if member_role is None:
            await ctx.send(
                "❌ The configured member role no longer exists."
            )
            return

        if channel is None:
            await ctx.send(
                "❌ The configured verification channel no longer exists."
            )
            return

        # Hide all channels from @everyone
        for guild_channel in ctx.guild.channels:

            if guild_channel == channel:
                continue

            await guild_channel.set_permissions(
                ctx.guild.default_role,
                view_channel=False,
                reason="Verification enabled"
            )

            await guild_channel.set_permissions(
                member_role,
                view_channel=True,
                reason="Verification enabled"
            )

        # Verification channel
        await channel.set_permissions(
            ctx.guild.default_role,
            view_channel=True,
            send_messages=False,
            read_message_history=True,
            reason="Verification enabled"
        )

        await channel.set_permissions(
            member_role,
            view_channel=False,
            reason="Verification enabled"
        )

        await channel.send(
            embed=discord.Embed(
                title="🔐 Server Verification",
                description=(
                    "Welcome!\n\n"
                    "Click **Verify** below to "
                    "access the server."
                )
            ),
            view=create_verification_view()
        )

        db.update(
            "server_config",
            "verification_enabled = ?",
            "guild_id = ?",
            (
                1,
                ctx.guild.id
            )
        )

        await ctx.send(
            "✅ Member verification is now **enabled**."
        )

        return

    db.update(
        "server_config",
        "verification_enabled = ?",
        "guild_id = ?",
        (
            0,
            ctx.guild.id
        )
    )

    await ctx.send(
        "✅ Member verification is now **disabled**."
    )


def setup(bot):
    bot.add_command(verification)