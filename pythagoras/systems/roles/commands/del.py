import discord
from discord import app_commands


@app_commands.command(
    name="delrole",
    description="Delete a server role."
)
@app_commands.describe(
    role="The role to delete."
)
async def delrole(
    interaction: discord.Interaction,
    role: discord.Role
):

    if role == interaction.guild.default_role:
        await interaction.response.send_message(
            "❌ I can't delete @everyone."
        )
        return

    if role >= interaction.guild.me.top_role:
        await interaction.response.send_message(
            "❌ I can't delete that role because "
            "it's higher than or equal to my "
            "highest role."
        )
        return

    role_name = role.name

    await role.delete(
        reason=f"Deleted by {interaction.user}"
    )

    await interaction.response.send_message(
        f"🗑️ Deleted role **{role_name}**."
    )


def setup(bot):
    bot.tree.add_command(delrole)