import discord
from discord import app_commands


@app_commands.command(
    name="ban",
    description="Ban a member from the server."
)
@app_commands.describe(
    member="The member you want to ban.",
    reason="Why the member is being banned."
)
@app_commands.default_permissions(ban_members=True)
async def ban(
    interaction: discord.Interaction,
    member: discord.Member,
    reason: str = "No reason provided."
):
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Missing Permission",
                description="You need **Ban Members** to use this command.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return

    if member.id == interaction.user.id:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Ban Failed",
                description="You can't ban yourself.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return

    if member.id == interaction.guild.owner_id:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Ban Failed",
                description="You can't ban the server owner.",
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
                title="❌ Ban Failed",
                description=(
                    "You can't ban a member with an equal or higher role."
                ),
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return

    if member.top_role >= interaction.guild.me.top_role:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Ban Failed",
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
        await member.ban(
            reason=f"{reason} | Banned by {interaction.user}"
        )
    except discord.Forbidden:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Ban Failed",
                description="I don't have permission to ban that member.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return
    except discord.HTTPException:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Ban Failed",
                description="Discord rejected the ban. Try again.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return

    embed = discord.Embed(
        title="🔨 Member Banned",
        description=f"{member.mention} has been banned.",
        color=discord.Color.red()
    )
    embed.add_field(name="Reason", value=reason, inline=False)
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text=f"Moderator: {interaction.user}")

    await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.tree.add_command(ban)
