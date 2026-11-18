import discord
import mycord

db = mycord.DB()

# profile embed function
def profile_embed(
    member, guild_id
):
    user_id = member.id
    claimed_character = db.fetchone(
        "character_claims",
        "guild_id = ? AND claimed_by = ?",
        (
            guild_id, user_id
        )
    )
    embed = discord.Embed(
        title=f"{member.display_name}'s Profile",
        description=f"**General Information**"
    )
    embed.set_thumbnail(
        url=member.display_avatar.url
    )
    joined = (
        discord.utils.format_dt(member.joined_at, style='R')
            if member.joined_at else "Unknown"
    )
    embed.add_field(
        name="📅 Joined:",
        value=joined,
        inline=True
        )
    
    return embed