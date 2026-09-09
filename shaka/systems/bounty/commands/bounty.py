import discord
from discord import app_commands
import aiohttp

from ..functions.get_bounty import get_bounty
from ..poster import create_poster


@app_commands.command(
    name="bounty",
    description="View a member's bounty."
)
@app_commands.describe(
    member="The member whose bounty you want to view."
)
async def bounty(
    interaction: discord.Interaction,
    member: discord.Member = None
):
    if member is None:
        member = interaction.user

    amount = get_bounty(
        interaction.guild.id,
        member.id
    )

    avatar_url = member.display_avatar.replace(
        size=512,
        format="png"
    ).url

    async with aiohttp.ClientSession() as session:
        async with session.get(avatar_url) as response:
            avatar_bytes = await response.read()

    poster = create_poster(
        member.display_name,
        amount,
        avatar_bytes
    )

    file = discord.File(
        poster,
        filename="wanted.png"
    )

    await interaction.response.send_message(
        file=file
    )


def setup(bot):
    bot.tree.add_command(bounty)