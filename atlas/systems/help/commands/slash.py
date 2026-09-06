from discord import app_commands
from ..views.help_view import HelpView


@app_commands.command(
    name="help",
    description="Show Atlas slash commands."
)
async def help_command(interaction):
    view = HelpView(interaction.client, interaction.user)

    await interaction.response.send_message(
        embed=view.embed(),
        view=view
    )


def setup(bot):
    bot.tree.add_command(help_command)