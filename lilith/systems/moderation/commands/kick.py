import discord
from discord import app_commands


@app_commands.command(
    name="kick",
    description="Kick a member from the server."
)
@app_commands.describe(
    member="The member you want to kick.",
    reason="Why the member is being kicked."
)
@app_commands.default_permissions(kick_members=True)
async def kick(
    interaction: discord.Interaction,
    member: discord.Member,
    reason: str = "No reason provided."
):
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Missing Permission",
                description="You need **Kick Members** to use this command.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return

    if member.id == interaction.user.id:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Kick Failed",
                description="You can't kick yourself.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return

    if member.id == interaction.guild.owner_id:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Kick Failed",
                description="You can't kick the server owner.",
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
                title="❌ Kick Failed",
                description=(
                    "You can't kick a member with an equal or higher role."
                ),
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return

    if member.top_role >= interaction.guild.me.top_role:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Kick Failed",
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
        await member.kick(
            reason=f"{reason} | Kicked by {interaction.user}"
        )
    except discord.Forbidden:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Kick Failed",
                description="I don't have permission to kick that member.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return
    except discord.HTTPException:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Kick Failed",
                description="Discord rejected the kick. Try again.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return

    embed = discord.Embed(
        title="👢 Member Kicked",
        description=f"{member.mention} has been kicked.",
        color=discord.Color.red()
    )
    embed.add_field(name="Reason", value=reason, inline=False)
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text=f"Moderator: {interaction.user}")

    await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.tree.add_command(kick)
