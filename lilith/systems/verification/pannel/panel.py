import discord

from .button import VerificationView


async def send_verification_panel(
    channel: discord.TextChannel
):
    embed = discord.Embed(
        title="🔐 Server Verification",
        description=(
            "Welcome to the server.\n\n"
            "Click the button below to verify yourself "
            "and gain access to the server."
        ),
        color=discord.Color.red()
    )

    await channel.send(
        embed=embed,
        view=VerificationView()
    )