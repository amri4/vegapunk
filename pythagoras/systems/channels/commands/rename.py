import discord
from discord import app_commands


@app_commands.command(
    name="renamechannel",
    description="Rename a channel."
)
@app_commands.describe(
    channel="The channel you want to rename.",
    name="The new name for the channel."
)
async def renamechannel(
    interaction: discord.Interaction,
    channel: discord.TextChannel,
    name: str
):
    name = name.strip()

    if not name:
        await interaction.response.send_message(
            "❌ Please specify a new name.",
            ephemeral=True
        )
        return

    old_name = channel.name

    await channel.edit(
        name=name,
        reason=f"Renamed by {interaction.user}"
    )

    await interaction.response.send_message(
        f"✅ Renamed **{old_name}** to **{name}**."
    )


def setup(bot):
    bot.tree.add_command(renamechannel)