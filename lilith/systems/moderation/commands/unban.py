import discord
from discord import app_commands


@app_commands.command(
    name="unban",
    description="Unban a user from the server."
)
@app_commands.describe(
    user_id="The ID of the user you want to unban.",
    reason="Why the user is being unbanned."
)
@app_commands.default_permissions(ban_members=True)
async def unban(
    interaction: discord.Interaction,
    user_id: str,
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

    if not user_id.isdigit():
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Unban Failed",
                description="That user ID is not valid.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return

    try:
        user = await interaction.client.fetch_user(int(user_id))
    except discord.NotFound:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Unban Failed",
                description="I couldn't find a user with that ID.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return
    except discord.HTTPException:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Unban Failed",
                description="Discord rejected the user lookup. Try again.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return

    try:
        await interaction.guild.unban(
            user,
            reason=f"{reason} | Unbanned by {interaction.user}"
        )
    except discord.NotFound:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Unban Failed",
                description=f"{user.mention} is not banned.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return
    except discord.Forbidden:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Unban Failed",
                description="I don't have permission to unban that user.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return
    except discord.HTTPException:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Unban Failed",
                description="Discord rejected the unban. Try again.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return

    embed = discord.Embed(
        title="🔓 User Unbanned",
        description=f"{user.mention} has been unbanned.",
        color=discord.Color.red()
    )
    embed.add_field(name="Reason", value=reason, inline=False)
    embed.set_thumbnail(url=user.display_avatar.url)
    embed.set_footer(text=f"Moderator: {interaction.user}")

    await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.tree.add_command(unban)
