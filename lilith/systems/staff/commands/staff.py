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
    rank TEXT,
    role_id INTEGER,
    PRIMARY KEY(guild_id, rank)
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

    if not mod:
        return None

    return mod[2]


async def get_staff_role(guild: discord.Guild, rank: str):

    role_data = db.fetchone(
        "staff_roles",
        "guild_id = ? AND rank = ?",
        (guild.id, rank)
    )

    if role_data:
        role = guild.get_role(role_data[2])

        if role:
            return role

        # The saved Discord role no longer exists
        db.delete(
            "staff_roles",
            "guild_id = ? AND rank = ?",
            (guild.id, rank)
        )

    # Create a new role
    role = await guild.create_role(
        name=rank,
        reason="Staff rank role"
    )

    db.insert(
        "staff_roles",
        "guild_id, rank, role_id",
        (guild.id, rank, role.id)
    )

    return role


staff_commands = app_commands.Group(
    name="staff",
    description="Community staff management"
)


@staff_commands.command(
    name="add",
    description="Add a member to the staff team"
)
async def add(
    interaction: discord.Interaction,
    member: discord.Member
):
    st_rank = "Support Team"
    
    staff_member = db.fetchone(
        "staff_members",
        "user_id = ? AND guild_id = ?",
        (member.id, interaction.guild.id)
    )

    if staff_member:
        await interaction.response.send_message(
            "This member is already a staff member."
        )
        return

    if member.bot:
        await interaction.response.send_message(
            "A bot can't be a staff member."
        )
        return

    actor = interaction.user
    joined = int(time.time())

    db.insert(
        "staff_members",
        "user_id, guild_id, rank, joined_at, added_by",
        (
            member.id,
            interaction.guild.id,
            st_rank,
            joined,
            actor.id
        )
    )

    role = await get_staff_role(interaction.guild, st_rank)
    rank = get_rank(member, interaction.guild)

    await member.add_roles(role)

    await interaction.response.send_message(
        f"{member.mention} has been added by "
        f"{actor.mention} as a **{rank}** staff member."
    )


@staff_commands.command(
    name="remove",
    description="Remove a member from the staff team"
)
async def remove(
    interaction: discord.Interaction,
    member: discord.Member
):
    mem = db.fetchone(
        "staff_members",
        "user_id = ? AND guild_id = ?",
        (member.id, interaction.guild.id)
    )

    if not mem:
        await interaction.response.send_message(
            "This member is not a staff member."
        )
        return

    role_data = db.fetchone(
        "staff_roles",
        "guild_id = ? AND rank = ?",
        (interaction.guild.id, mem[2])
    )

    if role_data:
        role = interaction.guild.get_role(role_data[2])

        if role:
            await member.remove_roles(role)

    db.delete(
        "staff_members",
        "user_id = ? AND guild_id = ?",
        (member.id, interaction.guild.id)
    )

    await interaction.response.send_message(
        f"{member.mention} is no longer a staff member."
    )


def setup(bot):
    bot.tree.add_command(staff_commands)
