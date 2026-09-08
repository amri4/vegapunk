import discord
from discord import app_commands

@app_commands.describe(
    players="Select players joining the game"
)
@app_commands.command(
    name="werewolf",
    description="play the werewolf game"
)
async def werewolf(
    interaction: discord.Interaction,
    players: str
):
    await interaction.response.send_message(
        f"{players}"
    )

 def setup(bot):
    bot.tree.add_command(werewolf)