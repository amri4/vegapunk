import discord
from discord import app_commands

import mycord

db = mycord.DB()

@app_commands.command(
    name="delpanel",
    description="delete an existing delpanel"
)
@app_commands.describe(
    ID="The panel id you want to delete"
)
async def delpanel(
    interaction: discord.Interaction, 
    ID: int
):
    panel = db.fetchone(
        "ticket_panels",
        "panel_id = ?",
        (ID,)
    )
    config = db.fetchone(
        "server_config",
        "guild_id = ?",
        (interaction.guild.id,)
    )
    channel_id = config[4]
    message_id = panel[2]
    channel = interaction.guild.get_channel(channel_id)
    message = await channel.fetch_message(message_id)
    await message.delete()
    
    db.delete(
        "ticket_panels",
        "panel_id = ?",
        (ID,)
    )
    await interaction.response.send_message(
        "✅️ Panel deleted",
        ephemeral=True
    )

def setup(bot):
    bot.tree.add_command(delpanel)