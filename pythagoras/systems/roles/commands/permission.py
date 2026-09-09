import discord
from discord import app_commands


@app_commands.command(
    name="rolepermission",
    description="Change a permission or setting for a server role."
)
@app_commands.describe(
    role="The role to change.",
    permission="The permission or setting to change.",
    state="Turn it on or off."
)
@app_commands.choices(
    permission=[
        app_commands.Choice(
            name="Administrator",
            value="administrator"
        ),
        app_commands.Choice(
            name="Manage Server",
            value="manage_guild"
        ),
        app_commands.Choice(
            name="Manage Channels",
            value="manage_channels"
        ),
        app_commands.Choice(
            name="Manage Roles",
            value="manage_roles"
        ),
        app_commands.Choice(
            name="Manage Messages",
            value="manage_messages"
        ),
        app_commands.Choice(
            name="Kick Members",
            value="kick_members"
        ),
        app_commands.Choice(
            name="Ban Members",
            value="ban_members"
        ),
        app_commands.Choice(
            name="Moderate Members",
            value="moderate_members"
        ),
        app_commands.Choice(
            name="Mention Everyone",
            value="mention_everyone"
        ),
        app_commands.Choice(
            name="View Audit Log",
            value="view_audit_log"
        ),
        app_commands.Choice(
            name="separate from members",
            value="hoist"
        ),
    ],
    state=[
        app_commands.Choice(
            name="On",
            value="on"
        ),
        app_commands.Choice(
            name="Off",
            value="off"
        ),
    ]
)
async def rolepermission(
    interaction: discord.Interaction,
    role: discord.Role,
    permission: app_commands.Choice[str],
    state: app_commands.Choice[str]
):

    if role == interaction.guild.default_role:
        await interaction.response.send_message(
            "❌ I can't change permissions for @everyone."
        )
        return

    if role >= interaction.guild.me.top_role:
        await interaction.response.send_message(
            "❌ I can't change that role because "
            "it's higher than or equal to my highest role."
        )
        return

    enabled = state.value == "on"

    if permission.value == "hoist":

        await role.edit(
            hoist=enabled,
            reason=f"Role setting changed by {interaction.user}"
        )

    else:

        permissions = role.permissions

        setattr(
            permissions,
            permission.value,
            enabled
        )

        await role.edit(
            permissions=permissions,
            reason=f"Permission changed by {interaction.user}"
        )

    await interaction.response.send_message(
        f"✅ **{permission.name}** turned "
        f"**{state.name}** for {role.mention}."
    )


def setup(bot):
    bot.tree.add_command(rolepermission)