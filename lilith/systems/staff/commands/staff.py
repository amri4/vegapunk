import discord
from discord import app_commands
import mycord
import time

db = mycord.DB()

db.create_table(
    "staff_members",
    """
    user_id INTEGER,
    guild_id INTEGER,
    rank TEXT,
    joined_at INTEGER,
    added_by INTEGER,
    PRIMARY KEY(user_id, guild_id)
    """
)
db.create_table(
    "staff_roles",
    """
    guild_id INTEGER,
    role_id INTEGER
    """
)

STAFF_RANKS = {
    "Head Administrator": 5,
    "Administrator": 4,
    "Senior Moderator": 3,
    "Moderator": 2,
    "Support Team": 1
}
def get_rank(member: discord.Member, guild: discord.Guild):
    mod = db.fetchone(
        "staff_members",
        "user_id = ? AND guild_id = ?",
        (member.id, guild.id)
    )
    return mod[2]

staff_commands = app_commands.Group(name="staff", description="Community staff management")

staff_commands.command(name="add", description="add a member to the staff team")
async def add(interaction: discord.Interaction, member: discord.Member):
    staff_member = db.fetchone(
        "staff_members",
        "user_id = ? AND guild_id = ?",
        (member.id, )
    )
    if staff_member:
        await interaction.response.send_message("This member is already a staff member")
        return
    if member.bot:
        await interaction.response.send_message("A bot can't be a staff member")
        return
    interaction.create_role

    actor = interaction.user
        
    joined = int(time.time())
    db.insert(
        "staff_members",
        "user_id, guild_id, rank, joined_at, added_by",
        (member, interaction.guild.id, "Support Team", joined, actor.id)
    )
    await interaction.response.send_message(f"{member.mention} has been added by {actor.mention} as a staff member")