import discord
from discord import app_commands

from ..functions.reaction_roles import start_reaction_role_setup


@app_commands.command(
    name="reactionroles",
    description="Create an interactive reaction role panel."
)
@app_commands.describe(
    channel="The channel where the panel will be sent."
)
@app_commands.default_permissions(manage_roles=True)
async def reactionroles(
    interaction: discord.Interaction,
    channel: discord.TextChannel
):
    await start_reaction_role_setup(
        interaction,
        channel
    )


def setup(bot):
    bot.tree.add_command(reactionroles)