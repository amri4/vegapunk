import discord
import mycord

from .get_claimed_characters import get_claimed_characters


db = mycord.DB()


async def update_panel(bot, guild_id):
    panel = db.fetchone(
        "character_panels",
        "guild_id = ?",
        (guild_id,)
    )

    if panel is None:
        return

    channel_id = panel[1]
    message_id = panel[2]

    channel = bot.get_channel(channel_id)

    if channel is None:
        return

    try:
        message = await channel.fetch_message(message_id)
    except discord.NotFound:
        return

    claims = get_claimed_characters(guild_id)

    embed = discord.Embed(
        title="🏴‍☠️ Character Claims",
        description="Characters currently claimed in this server.",
        color=discord.Color.gold()
    )

    if not claims:
        embed.description = "No characters have been claimed yet."
    else:
        for claim in claims:
            character_name = claim[1]
            user_id = claim[2]

            embed.add_field(
                name=character_name,
                value=f"<@{user_id}>",
                inline=False
            )

    await message.edit(embed=embed)