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
        title=f"{member.mention}'s' Profile",
        description=f"**General Information**"
    )
    embed.set_thumbnail(
        url=member.display_avatar.url
    )
    embed.add_field(
        name="📅 Joined:",
        value=f"`{discord.utils.format_dt(member.joined_at, style='R')}`\n"
        )
    
    return embed