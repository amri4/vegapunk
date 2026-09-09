import discord
from discord import app_commands


@app_commands.command(
    name="channelpermission",
    description="Change a role's permission in a channel."
)
@app_commands.describe(
    channel="The channel to change.",
    role="The role whose permission you want to change.",
    permission="The permission to change.",
    state="Turn the permission on or off."
)
@app_commands.choices(
    permission=[
        app_commands.Choice(name="View Channel", value="view_channel"),
        app_commands.Choice(name="Send Messages", value="send_messages"),
        app_commands.Choice(name="Manage Messages", value="manage_messages"),
        app_commands.Choice(name="Embed Links", value="embed_links"),
        app_commands.Choice(name="Attach Files", value="attach_files"),
        app_commands.Choice(name="Add Reactions", value="add_reactions"),
        app_commands.Choice(name="Read Message History", value="read_message_history"),
        app_commands.Choice(name="Mention Everyone", value="mention_everyone"),
        app_commands.Choice(name="Connect", value="connect"),
        app_commands.Choice(name="Speak", value="speak"),
    ],
    state=[
        app_commands.Choice(name="On", value="on"),
        app_commands.Choice(name="Off", value="off"),
    ]
)
async def channelpermission(
    interaction: discord.Interaction,
    channel: discord.abc.GuildChannel,
    role: discord.Role,
    permission: app_commands.Choice[str],
    state: app_commands.Choice[str]
):

    overwrite = channel.overwrites_for(role)

    setattr(
        overwrite,
        permission.value,
        state.value == "on"
    )

    await channel.set_permissions(
        role,
        overwrite=overwrite,
        reason=f"Permission changed by {interaction.user}"
    )

    await interaction.response.send_message(
        f"✅ **{permission.name}** turned "
        f"**{state.name}** for {role.mention} "
        f"in {channel.mention}."
    )


def setup(bot):
    bot.tree.add_command(channelpermission)