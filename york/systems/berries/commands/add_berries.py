import discord
from discord import app_commands
from york.systems.berries.functions.berries import add_berries

@app_commands.command(
    name="give_berries"
    description="give member berries"
)
async def give_berries(
    interaction: discord.interaction,
    amount: int,
    member: discord.Member
):
    
    await add_berries(
        interaction.guild.id,
        member,
        amount
    )
    await interaction.response.send_message(
        f"Added **{amount}** to **{member.display_name}'s** balance."
    )