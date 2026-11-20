import discord
from discord import app_commands


@app_commands.command(
    name="untimeout",
    description="Remove a timeout from a member."
)
@app_commands.describe(
    member="The member whose timeout you want to remove."
)
@app_commands.default_permissions(moderate_members=True)
async def untimeout(
    interaction: discord.Interaction,
    member: discord.Member
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
                title="❌ Untimeout Failed",
                description="You can't remove your own timeout.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return

    if member.id == interaction.guild.owner_id:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Untimeout Failed",
                description="You can't change the server owner's timeout.",
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
                title="❌ Untimeout Failed",
                description=(
                    "You can't remove a timeout from a member "
                    "with an equal or higher role."
                ),
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return

    if member.top_role >= interaction.guild.me.top_role:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Untimeout Failed",
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
            None,
            reason=f"Timeout removed by {interaction.user}"
        )
    except discord.Forbidden:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Untimeout Failed",
                description="I don't have permission to remove that timeout.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return
    except discord.HTTPException:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Untimeout Failed",
                description="Discord rejected the timeout removal. Try again.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return

    embed = discord.Embed(
        title="⏳ Timeout Removed",
        description=f"{member.mention} is no longer timed out.",
        color=discord.Color.red()
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text=f"Moderator: {interaction.user}")

    await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.tree.add_command(untimeout)
