import traceback

from discord import app_commands
from ..views.help_view import HelpView


@app_commands.command(
    name="help",
    description="Show Atlas slash commands."
)
async def help_command(interaction):

    try:
        view = HelpView(interaction.client, interaction.user)

        await interaction.response.send_message(
            embed=await view.embed(),
            view=view
        )

    except Exception as error:
        print("[HELP ERROR]")
        traceback.print_exc()

        if not interaction.response.is_done():
            await interaction.response.send_message(
                f"Help command error: `{type(error).__name__}`",
                ephemeral=True
            )


def setup(bot):
    bot.tree.add_command(help_command)