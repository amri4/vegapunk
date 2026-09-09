import discord
from discord import app_commands

from ..functions.get_bounty import get_bounty


@app_commands.command(
    name="bounty",
    description="View a member's bounty."
)
@app_commands.describe(
    member="The member whose bounty you want to view."
)
async def bounty(
    interaction: discord.Interaction,
    member: discord.Member = None
):
    if member is None:
        member = interaction.user

    amount = get_bounty(
        interaction.guild.id,
        member.id
    )

    await interaction.response.send_message(
        f"🏴‍☠️ **{member.display_name}'s Bounty:** "
        f"💰 {amount:,}"
    )


def setup(bot):
    bot.tree.add_command(bounty)