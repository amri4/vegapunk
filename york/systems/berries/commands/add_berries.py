import discord
from discord import app_commands
from york.systems.berries.functions.berries import add_berries

@app_commands.command(
    name="give_berries",
    description="give member berries"
)
@app_commands.checks.has_permission(administrator=True)
async def give_berries(
    interaction: discord.Interaction,
    amount: int,
    member: discord.Member
):
    if amount = 0:
        await interaction.response.send_message(
            "You can't give someone zero berries bruh 😭"
        )
        return
    
    await add_berries(
        interaction.guild.id,
        member,
        amount
    )
    await interaction.response.send_message(
        f"✅ Added **{amount:,}** to **{member.display_name}'s** balance."
    )