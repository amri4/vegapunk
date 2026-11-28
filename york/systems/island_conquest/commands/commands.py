import discord
from discord import app_commands
import mycord

db = mycord.DB()

db.create_table(
    "profiles",
    """
    user_id INTEGER,
    guild_id INTEGER,
    island_name TEXT,
    PRIMARY KEY(user_id, guild_id)
    """
)
conquest_commands = app_commands.Group(
    name="conquest",
    description="island conquest commands"
)

conquest_commands.command(
    name="create_profile",
    description="create your island conquest profile"
)
async def create_profile(
    interaction: discord.Interaction,
    island_name: str
):
    player_exists = db.fetchone(
        "profiles",
        "user_id = ? AND guild_id = ?",
        (interaction.user.id, interaction.guild.id)
    )
    if player_exists:
        await interaction.response.send_message(
            "You already have a profile",
            ephemeral=True
        )
        return
    db.insert(
        "profiles",
        "user_id, guild_id, island_name",
        (interaction.user.id, interaction.guild.id, island_name)
    )
    