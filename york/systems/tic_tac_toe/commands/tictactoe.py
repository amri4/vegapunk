import discord
from discord import app_commands

from ..views.game import TicTacToeView


@app_commands.command(
    name="tictactoe",
    description="Play Tic Tac Toe with another member."
)
async def tictactoe(
    interaction: discord.Interaction,
    member: discord.Member
):
    if member.bot:
        await interaction.response.send_message(
            "❌ You can't play against a bot.",
            ephemeral=True
        )
        return

    if member.id == interaction.user.id:
        await interaction.response.send_message(
            "❌ You can't play against yourself.",
            ephemeral=True
        )
        return

    view = TicTacToeView(
        player_x=interaction.user.id,
        player_o=member.id
    )

    await interaction.response.send_message(
        f"❌ {interaction.user.mention} vs ⭕ {member.mention}\n\n"
        f"🎮 **{interaction.user.display_name} goes first!**",
        view=view
    )


def setup(bot):
    bot.tree.add_command(tictactoe)