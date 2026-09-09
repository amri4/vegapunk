import discord
from discord import app_commands


@app_commands.command(
    name="giverole",
    description="Give a role to a member."
)
@app_commands.describe(
    member="The member to give the role to.",
    role="The role to give."
)
async def giverole(
    interaction: discord.Interaction,
    member: discord.Member,
    role: discord.Role
):

    if role == interaction.guild.default_role:
        await interaction.response.send_message(
            "❌ I can't assign @everyone."
        )
        return

    if role >= interaction.guild.me.top_role:
        await interaction.response.send_message(
            "❌ I can't assign that role because "
            "it's higher than or equal to my "
            "highest role."
        )
        return

    if role in member.roles:
        await interaction.response.send_message(
            f"❌ {member.mention} already has "
            f"{role.mention}."
        )
        return

    await member.add_roles(
        role,
        reason=f"Role given by {interaction.user}"
    )

    await interaction.response.send_message(
        f"✅ Added {role.mention} to "
        f"{member.mention}."
    )


def setup(bot):
    bot.tree.add_command(giverole)