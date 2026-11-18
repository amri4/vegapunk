import discord
from discord import app_commands

from shaka.systems.profile.functions.embed import profile_embed

@app_commands.command(
    name="Profile"
    description="View your or others Profile."
)
async def profile(
    interaction: discord.Interaction,
    member: discord.Member = None
)
member = member or interaction.user

embed = profile_embed(
    member,
    interaction.guild_id
)

await interaction.response.send_message(
    embed=embed
)