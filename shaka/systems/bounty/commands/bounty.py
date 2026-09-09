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

    embed = discord.Embed(
        title="🏴‍☠️ WANTED",
        description=(
            f"## {member.display_name}\n"
            f"**☠️ DEAD OR ALIVE**"
        ),
        color=discord.Color.dark_red()
    )

    embed.set_thumbnail(
        url=member.display_avatar.url
    )

    embed.add_field(
        name="💰 BOUNTY",
        value=f"**{amount:,} BERRIES**",
        inline=False
    )

    embed.set_footer(
        text="Shaka • Grand Era Bounty System"
    )

    await interaction.response.send_message(
        embed=embed
    )


def setup(bot):
    bot.tree.add_command(bounty)