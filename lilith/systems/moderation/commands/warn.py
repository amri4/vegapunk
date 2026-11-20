import discord
import mycord
from discord import app_commands


db = mycord.DB()

db.create_table(
    "warnings",
    """
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guild_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    moderator_id INTEGER NOT NULL,
    reason TEXT NOT NULL,
    created_at TEXT NOT NULL
    """
)


@app_commands.command(
    name="warn",
    description="Warn a member."
)
@app_commands.describe(
    member="The member you want to warn.",
    reason="Why the member is being warned."
)
@app_commands.default_permissions(moderate_members=True)
async def warn(
    interaction: discord.Interaction,
    member: discord.Member,
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
                title="❌ Warn Failed",
                description="You can't warn yourself.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return

    if member.id == interaction.guild.owner_id:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Warn Failed",
                description="You can't warn the server owner.",
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
                title="❌ Warn Failed",
                description=(
                    "You can't warn a member with an equal or higher role."
                ),
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return

    if member.top_role >= interaction.guild.me.top_role:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Warn Failed",
                description=(
                    "Their role is equal to or above mine. "
                    "Move my role higher and try again."
                ),
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return

    db.insert(
        "warnings",
        "guild_id, user_id, moderator_id, reason, created_at",
        (
            interaction.guild.id,
            member.id,
            interaction.user.id,
            reason,
            discord.utils.utcnow().isoformat()
        )
    )

    embed = discord.Embed(
        title="⚠️ Member Warned",
        description=f"{member.mention} has been warned.",
        color=discord.Color.red()
    )
    embed.add_field(name="Reason", value=reason, inline=False)
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text=f"Moderator: {interaction.user}")

    await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.tree.add_command(warn)
