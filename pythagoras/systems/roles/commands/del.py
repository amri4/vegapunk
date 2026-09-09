import discord
from discord import app_commands

from ..functions.find_role import find_role


@app_commands.command(
    name="delrole",
    description="Delete a server role."
)
@app_commands.describe(
    name="The name of the role to delete."
)
async def delrole(
    interaction: discord.Interaction,
    name: str
):

    result = find_role(
        interaction.guild,
        name
    )

    if result is None:
        await interaction.response.send_message(
            "❌ I couldn't find that role."
        )
        return

    if isinstance(result, list):

        names = "\n".join(
            f"• {role.mention}"
            for role in result[:10]
        )

        await interaction.response.send_message(
            "❌ Multiple roles found:\n"
            + names
        )
        return

    role = result

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