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


async def change_staff_rank(interaction, member, direction):

    guild = interaction.guild

    # Get staff record
    staff = db.fetchone(
        "staff_members",
        "user_id = ? AND guild_id = ?",
        (member.id, guild.id)
    )

    if not staff:
        await interaction.response.send_message(
            "This member is not a staff member."
        )
        return

    current_rank = staff[2]

    current_level = STAFF_RANKS.get(current_rank)

    if current_level is None:
        await interaction.response.send_message(
            "This member has an invalid staff rank."
        )
        return

    # Find the new rank
    new_level = current_level + direction

    new_rank = next(
        (
            rank
            for rank, level in STAFF_RANKS.items()
            if level == new_level
        ),
        None
    )

    if new_rank is None:
        await interaction.response.send_message(
            "This member is already at the highest or lowest rank."
        )
        return

    await interaction.response.defer()

    try:
        # Get both roles
        old_role = await get_staff_role(guild, current_rank)
        new_role = await get_staff_role(guild, new_rank)

        # Change Discord roles
        await member.add_roles(new_role)
        await member.remove_roles(old_role)

        # Update database
        db.update(
            "staff_members",
            "rank = ?",
            "user_id = ? AND guild_id = ?",
            (new_rank, member.id, guild.id)
        )

        await interaction.followup.send(
            f"{member.mention} has been "
            f"{'promoted' if direction == 1 else 'demoted'} "
            f"from **{current_rank}** to **{new_rank}**."
        )

    except discord.HTTPException:
        await interaction.followup.send(
            "I couldn't update the member's Discord roles. "
            "Check my role permissions and hierarchy."
        )


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
    print("STAFF RECORD:", mem, flush=True)
    role_data = db.fetchone(
        "staff_roles",
        "guild_id = ? AND rank = ?",
        (interaction.guild.id, mem[2])
    )
    print("ROLE DATA:", role_data, flush=True)

    if role_data:
        role = interaction.guild.get_role(role_data[2])
        print("ROLE:", role, flush=True)

        if role:
            await member.remove_roles(role)
    print("DELETING DATABASE RECORD", flush=True)
    try:
        db.delete(
            "staff_members",
            "user_id = ? AND guild_id = ?",
            (member.id, interaction.guild.id)
        )
        print("DATABASE RECORD DELETED", flush=True)
    except Exception as e:
        print(f"DELETE ERROR: {type(e).__name__}: {e}", flush=True)

    await interaction.response.send_message(
        f"{member.mention} is no longer a staff member."
    )


@staff_commands.command(
    name="promote",
    description="Promote a staff member"
)
async def promote(interaction: discord.Interaction, member: discord.Member):

    await change_staff_rank(
        interaction,
        member,
        1
    )


@staff_commands.command(
    name="demote",
    description="Demote a staff member"
)
async def demote(interaction: discord.Interaction, member: discord.Member):

    await change_staff_rank(
        interaction,
        member,
        -1
    )


def setup(bot):
    bot.tree.add_command(staff_commands)
