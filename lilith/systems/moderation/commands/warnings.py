import random

import discord
import mycord
from discord import app_commands


db = mycord.DB()


@app_commands.command(
    name="warnings",
    description="View a member's warnings."
)
@app_commands.describe(
    member="The member whose warnings you want to view."
)
@app_commands.default_permissions(moderate_members=True)
async def warnings(
    interaction: discord.Interaction,
    member: discord.Member
):
    warning_list = db.fetchall("warnings")

    user_warnings = [
        warning
        for warning in warning_list
        if warning[1] == member.id
        and warning[0] is not None
    ]

    if not user_warnings:
        responses = [
            f"{member.mention} has no warnings. Don't ruin that.",
            f"Tch. {member.mention} has a clean record.",
            f"No warnings for {member.mention}. Surprisingly."
        ]

        await interaction.response.send_message(random.choice(responses))
        return

    lines = []

    for warning in user_warnings:
        warning_id = warning[0]
        moderator_id = warning[2]
        reason = warning[3]
        created_at = warning[4]

        lines.append(
            f"**#{warning_id}** — {reason}\n"
            f"Moderator: <@{moderator_id}>\n"
            f"Date: `{created_at}`"
        )

    embed = discord.Embed(
        title=f"🩸 Warnings — {member}",
        description="\n\n".join(lines),
        color=discord.Color.red()
    )

    embed.set_thumbnail(url=member.display_avatar.url)

    await interaction.response.send_message(
        embed=embed
    )


def setup(bot):
    bot.tree.add_command(warnings)