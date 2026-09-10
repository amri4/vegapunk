import discord
from discord import app_commands


@app_commands.command(
    name="moverole",
    description="Move a role above or below another role."
)
@app_commands.describe(
    role="The role to move.",
    position="Move the role above or below the target.",
    target="The role to move relative to."
)
@app_commands.choices(
    position=[
        app_commands.Choice(
            name="Above",
            value="above"
        ),
        app_commands.Choice(
            name="Below",
            value="below"
        )
    ]
)
async def moverole(
    interaction: discord.Interaction,
    role: discord.Role,
    position: app_commands.Choice[str],
    target: discord.Role
):

    position = position.value

    if role == interaction.guild.default_role:
        await interaction.response.send_message(
            "❌ I can't move @everyone."
        )
        return

    if target == interaction.guild.default_role:
        await interaction.response.send_message(
            "❌ You can't move a role relative to @everyone."
        )
        return

    if role == target:
        await interaction.response.send_message(
            "❌ The two roles must be different."
        )
        return

    bot_role = interaction.guild.me.top_role

    if role >= bot_role:
        await interaction.response.send_message(
            "❌ I can't move that role because "
            "it's higher than or equal to my highest role."
        )
        return

    if target >= bot_role:
        await interaction.response.send_message(
            "❌ I can't move a role relative to "
            "a role that's higher than or equal "
            "to my highest role."
        )
        return

    if position == "above":

        if role.position < target.position:
            new_position = target.position

        else:
            new_position = target.position + 1

    else:

        if role.position > target.position:
            new_position = target.position

        else:
            new_position = target.position - 1

    new_position = max(
        1,
        min(
            new_position,
            bot_role.position - 1
        )
    )

    await interaction.guild.edit_role_positions(
        positions={
            role: new_position
        },
        reason=f"Moved by {interaction.user}"
    )

    await interaction.response.send_message(
        f"↕️ Moved {role.mention} "
        f"**{position}** {target.mention}."
    )


def setup(bot):
    bot.tree.add_command(moverole)