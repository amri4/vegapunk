import discord
from discord import app_commands


@app_commands.command(
    name="addrole",
    description="Create a new server role."
)
@app_commands.describe(
    name="The name of the new role."
)
async def addrole(
    interaction: discord.Interaction,
    name: str
):

    name = name.strip()

    if not name:
        await interaction.response.send_message(
            "❌ Please provide a role name."
        )
        return

    role = await interaction.guild.create_role(
        name=name,
        reason=f"Created by {interaction.user}"
    )

    await interaction.response.send_message(
        f"✅ Created role {role.mention}."
    )


def setup(bot):
    bot.tree.add_command(addrole)