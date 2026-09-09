import discord
from discord import app_commands

from utils.role_colors import parse_role_color


@app_commands.command(
    name="setrolecolor",
    description="Change the color of a server role."
)
@app_commands.describe(
    role="The role whose color you want to change.",
    color="The color name or hex code."
)
async def setrolecolor(
    interaction: discord.Interaction,
    role: discord.Role,
    color: str
):

    if role == interaction.guild.default_role:
        await interaction.response.send_message(
            "❌ I can't change the color of @everyone."
        )
        return

    if role >= interaction.guild.me.top_role:
        await interaction.response.send_message(
            "❌ I can't change that role because "
            "it's higher than or equal to my "
            "highest role."
        )
        return

    parsed_color = parse_role_color(color)

    if parsed_color is None:
        await interaction.response.send_message(
            "❌ Invalid color.\n\n"
            "Use a color name such as "
            "`red`, `crimson`, `cyan`, "
            "`gold`, `lavender`, etc.\n\n"
            "Or use a hex code such as "
            "`#5865F2`."
        )
        return

    await role.edit(
        color=discord.Color(parsed_color),
        reason=f"Color changed by {interaction.user}"
    )

    await interaction.response.send_message(
        f"🎨 Changed {role.mention} to `{color}`."
    )


def setup(bot):
    bot.tree.add_command(setrolecolor)