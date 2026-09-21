import discord
from discord import app_commands

from ..functions.trades import create_trade


@app_commands.command(
    name="trade",
    description="Start a trade with another member."
)
async def trade(
    interaction: discord.Interaction,
    member: discord.Member
):
    if member.bot:
        await interaction.response.send_message(
            "❌ You can't trade with a bot.",
            ephemeral=True
        )
        return

    if member.id == interaction.user.id:
        await interaction.response.send_message(
            "❌ You can't trade with yourself.",
            ephemeral=True
        )
        return

    trade_id = create_trade(
        interaction.guild.id,
        interaction.user.id,
        member.id
    )

    await interaction.response.send_message(
        f"🤝 Trade **#{trade_id}** started with {member.mention}!"
    )


def setup(bot):
    bot.tree.add_command(
        trade
    )