import discord
from discord import app_commands


@app_commands.command(
    name="takerole",
    description="Remove a role from a member."
)
@app_commands.describe(
    member="The member to remove the role from.",
    role="The role to remove."
)
async def takerole(
    interaction: discord.Interaction,
    member: discord.Member,
    role: discord.Role
):

    if role == interaction.guild.default_role:
        await interaction.response.send_message(
            "❌ I can't remove @everyone."
        )
        return

    if role >= interaction.guild.me.top_role:
        await interaction.response.send_message(
            "❌ I can't remove that role because "
            "it's higher than or equal to my "
            "highest role."
        )
        return

    if role not in member.roles:
        await interaction.response.send_message(
            f"❌ {member.mention} doesn't have "
            f"{role.mention}."
        )
        return

    await member.remove_roles(
        role,
        reason=f"Role removed by {interaction.user}"
    )

    await interaction.response.send_message(
        f"✅ Removed {role.mention} from "
        f"{member.mention}."
    )


def setup(bot):
    bot.tree.add_command(takerole)