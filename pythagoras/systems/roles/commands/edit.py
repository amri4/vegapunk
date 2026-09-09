import discord
from discord import app_commands

from ..functions.find_role import find_role


@app_commands.command(
    name="editrole",
    description="Rename an existing server role."
)
@app_commands.describe(
    role="The role to rename.",
    name="The new name for the role."
)
async def editrole(
    interaction: discord.Interaction,
    role: str,
    name: str
):

    result = find_role(
        interaction.guild,
        role
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
            "❌ I can't edit @everyone."
        )
        return

    if role >= interaction.guild.me.top_role:
        await interaction.response.send_message(
            "❌ I can't edit that role because "
            "it's higher than or equal to my "
            "highest role."
        )
        return

    name = name.strip()

    if not name:
        await interaction.response.send_message(
            "❌ Please provide a new role name."
        )
        return

    old_name = role.name

    await role.edit(
        name=name,
        reason=f"Edited by {interaction.user}"
    )

    await interaction.response.send_message(
        f"✏️ Renamed **{old_name}** → "
        f"{role.mention}."
    )


def setup(bot):
    bot.tree.add_command(editrole)