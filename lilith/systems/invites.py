import os
import discord
from discord import app_commands


BOT_IDS = {
    "Lilith": os.getenv("LILITH_APPLICATION_ID"),
    "Shaka": os.getenv("SHAKA_APPLICATION_ID"),
    "Pythagoras": os.getenv("PYTHAGORAS_APPLICATION_ID"),
    "Atlas": os.getenv("ATLAS_APPLICATION_ID"),
    "York": os.getenv("YORK_APPLICATION_ID"),
    "Edison": os.getenv("EDISON_APPLICATION_ID"),
}


def invite_url(application_id):
    return (
        "https://discord.com/oauth2/authorize"
        f"?client_id={application_id}"
        "&scope=bot%20applications.commands"
        "&permissions=0"
    )


class InviteView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)

        for name, application_id in BOT_IDS.items():
            if not application_id:
                continue

            self.add_item(
                discord.ui.Button(
                    label=f"Invite {name}",
                    url=invite_url(application_id),
                    style=discord.ButtonStyle.link
                )
            )


@app_commands.command(
    name="invite",
    description="Get invite links for the bot fleet."
)
async def invite(interaction: discord.Interaction):

    bot = interaction.client
    owner = bot.application.owner

    if owner is None:
        await interaction.response.send_message(
            "❌ I couldn't determine the bot owner.",
            ephemeral=True
        )
        return

    if interaction.user.id != owner.id:
        await interaction.response.send_message(
            "❌ Only the bot owner can use this command.",
            ephemeral=True
        )
        return

    embed = discord.Embed(
        title="🤖 Bot Invites",
        description="Choose a bot to invite it to a server.",
        color=discord.Color.blurple()
    )

    await interaction.response.send_message(
        embed=embed,
        view=InviteView(),
        ephemeral=True
    )


def setup(bot):
    bot.tree.add_command(invite)