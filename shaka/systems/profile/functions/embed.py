import discord
import mycord

db = mycord.DB()

# profile embed function
def profile_embed(
    user_id, guild_id
):
    claimed_character = db.fetchone(
        "character_claims",
        "guild_id = ? AND claimed_by = ?",
        (
            guild_id, user_id
        )
    )
    embed = discord.Embed(
        title="User Profile"
    )
    