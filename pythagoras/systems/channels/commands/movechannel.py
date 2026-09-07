import discord
from discord import app_commands


@app_commands.command(
    name="movechannel",
    description="Move a channel above or below another channel."
)
@app_commands.describe(
    channel="The channel you want to move.",
    direction="Move it above or below the target.",
    target="The channel to move relative to."
)
@app_commands.choices(
    direction=[
        app_commands.Choice(
            name="Above",
            value="above"
        ),
        app_commands.Choice(
            name="Below",
            value="below"
        )
    ]
)
async def movechannel(
    interaction: discord.Interaction,
    channel: discord.TextChannel,
    direction: app_commands.Choice[str],
    target: discord.TextChannel
):
    if channel.id == target.id:
        await interaction.response.send_message(
            "❌ You can't move a channel relative to itself.",
            ephemeral=True
        )
        return

    if channel.category_id != target.category_id:
        await interaction.response.send_message(
            "❌ Both channels must be in the same category.",
            ephemeral=True
        )
        return

    target_position = target.position

    if direction.value == "above":
        new_position = target_position
    else:
        new_position = target_position + 1

    await channel.edit(
        position=new_position,
        reason=f"Moved by {interaction.user}"
    )

    await interaction.response.send_message(
        f"📁 Moved {channel.mention} "
        f"**{direction.value}** {target.mention}."
    )


def setup(bot):
    bot.tree.add_command(movechannel)