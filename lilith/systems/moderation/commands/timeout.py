from datetime import timedelta

import discord
from discord import app_commands


@app_commands.command(
    name="timeout",
    description="Timeout a member."
)
@app_commands.describe(
    member="The member you want to timeout.",
    duration="How long the timeout should last in minutes.",
    reason="Why the member is being timed out."
)
@app_commands.default_permissions(moderate_members=True)
async def timeout(
    interaction: discord.Interaction,
    member: discord.Member,
    duration: app_commands.Range[int, 1, 40320],
    reason: str = "No reason provided."
):
    if not interaction.user.guild_permissions.moderate_members:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Missing Permission",
                description="You need **Moderate Members** to use this command.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return

    if member.id == interaction.user.id:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Timeout Failed",
                description="You can't timeout yourself.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return

    if member.id == interaction.guild.owner_id:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Timeout Failed",
                description="You can't timeout the server owner.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return

    if (
        interaction.user.id != interaction.guild.owner_id
        and member.top_role >= interaction.user.top_role
    ):
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Timeout Failed",
                description=(
                    "You can't timeout a member with an equal or higher role."
                ),
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return

    if member.top_role >= interaction.guild.me.top_role:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Timeout Failed",
                description=(
                    "Their role is equal to or above mine. "
                    "Move my role higher and try again."
                ),
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return

    try:
        await member.timeout(
            discord.utils.utcnow() + timedelta(minutes=duration),
            reason=f"{reason} | Timed out by {interaction.user}"
        )
    except discord.Forbidden:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Timeout Failed",
                description="I don't have permission to timeout that member.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return
    except discord.HTTPException:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Timeout Failed",
                description="Discord rejected the timeout. Try again.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return

    embed = discord.Embed(
        title="⏳ Member Timed Out",
        description=f"{member.mention} has been timed out.",
        color=discord.Color.red()
    )
    embed.add_field(
        name="Duration",
        value=f"{duration} minute(s)",
        inline=True
    )
    embed.add_field(name="Reason", value=reason, inline=False)
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text=f"Moderator: {interaction.user}")

    await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.tree.add_command(timeout)
