import discord
from discord import app_commands


@app_commands.command(
    name="purge",
    description="Delete a number of recent messages."
)
@app_commands.describe(
    amount="The number of messages to delete.",
    member="Only delete messages from this member."
)
@app_commands.default_permissions(manage_messages=True)
async def purge(
    interaction: discord.Interaction,
    amount: app_commands.Range[int, 1, 100],
    member: discord.Member = None
):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Missing Permission",
                description="You need **Manage Messages** to use this command.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return

    channel = interaction.channel

    if not isinstance(channel, (discord.TextChannel, discord.Thread)):
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Purge Failed",
                description="This command only works in text channels.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return

    if member is not None:
        if member.id == interaction.guild.owner_id:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="❌ Purge Failed",
                    description="You can't purge the server owner's messages.",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return

        if (
            member.id != interaction.user.id
            and interaction.user.id != interaction.guild.owner_id
            and member.top_role >= interaction.user.top_role
        ):
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="❌ Purge Failed",
                    description=(
                        "You can't purge messages from a member "
                        "with an equal or higher role."
                    ),
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return

    await interaction.response.defer(ephemeral=True)

    def from_member(message):
        return member is None or message.author.id == member.id

    try:
        deleted = await channel.purge(limit=amount, check=from_member)
    except discord.Forbidden:
        await interaction.followup.send(
            embed=discord.Embed(
                title="❌ Purge Failed",
                description="I don't have permission to delete messages here.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return
    except discord.HTTPException:
        await interaction.followup.send(
            embed=discord.Embed(
                title="❌ Purge Failed",
                description="Discord rejected the purge. Try again.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
        return

    description = f"Deleted **{len(deleted)}** message(s) in {channel.mention}."

    if member is not None:
        description = (
            f"Deleted **{len(deleted)}** message(s) from "
            f"{member.mention} in {channel.mention}."
        )

    embed = discord.Embed(
        title="🧹 Messages Purged",
        description=description,
        color=discord.Color.red()
    )
    embed.set_footer(text=f"Moderator: {interaction.user}")

    await interaction.followup.send(embed=embed, ephemeral=True)


def setup(bot):
    bot.tree.add_command(purge)
