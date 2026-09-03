from discord.ext import commands

from ...config.functions.get_config import get_config
from ...config.tables import db


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

    get_config(ctx.guild)

    enabled = 1 if state == "on" else 0

    db.add_column(
        "server_config",
        "verification_enabled",
        "INTEGER"
    )

    db.update(
        "server_config",
        "verification_enabled = ?",
        "guild_id = ?",
        (
            enabled,
            ctx.guild.id
        )
    )

    status = "enabled" if enabled else "disabled"

    await ctx.send(
        f"✅ Member verification is now **{status}**."
    )


def setup(bot):
    bot.add_command(verification)