import discord
from discord import app_commands

from ..functions.add_strike import add_strike
from ..functions.prison import imprison
from ..ids import STRIKE_CHANNEL_ID


@app_commands.command(
    name="warn",
    description="Give a member a strike."
)
@app_commands.describe(
    member="The member you want to warn.",
    reason="Why they are receiving the strike."
)
@app_commands.default_permissions(moderate_members=True)
async def warn(
    interaction: discord.Interaction,
    member: discord.Member,
    reason: str
):
    strikes = add_strike(
        interaction.guild.id,
        member.id
    )

    channel = interaction.guild.get_channel(STRIKE_CHANNEL_ID)

    if strikes >= 5:
        imprison(
            interaction.guild.id,
            member.id,
            86400
        )

        message = (
            f"🚨 **5/5 Strikes**\n"
            f"{member.mention} has been sent to prison for **24 hours**.\n"
            f"**Reason:** {reason}"
        )
    else:
        message = (
            f"⚠️ **Strike {strikes}/5**\n"
            f"{member.mention} has received a strike.\n"
            f"**Reason:** {reason}"
        )

    if channel is not None:
        await channel.send(message)

    await interaction.response.send_message(
        f"✅ {member.mention} received strike **{strikes}/5**."
    )


def setup(bot):
    bot.tree.add_command(warn)