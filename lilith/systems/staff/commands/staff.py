import discord
from discord import app_commands
import mycord
import time

db = mycord.DB()

#========TABLES========
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

db.create_table(
    "staff_panel",
    """
    guild_id INTEGER PRIMARY KEY,
    channel_id INTEGER,
    message_id INTEGER,
    enabled INTEGER
    """
)

#========RANKS========
STAFF_RANKS = {
    "Head Administrator": 5,
    "Administrator": 4,
    "Senior Moderator": 3,
    "Moderator": 2,
    "Support Team": 1
}

#========BUTTONS========
class StaffPanel(discord.ui.View):

    def __init__(self, enabled=True):
        super().__init__(timeout=None)

        self.join_button.disabled = not enabled
        self.join_button.disabled = not enabled

        if enabled:
            self.join_button.label = "Join Staff"
            self.join_button.style = discord.ButtonStyle.success
            self.join_button.emoji = "➕"
        else:
            self.join_button.label = "Currently Closed"
            self.join_button.style = discord.ButtonStyle.danger
            self.join_button.emoji = "⛔"

    @discord.ui.button(
        label="Join Staff",
        style=discord.ButtonStyle.primary,
        custom_id="staff:join"
    )
    async def join_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_message(
            "You clicked the staff button!",
            ephemeral=True
        )

#========FUNCTIONS========
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

#========COMMANDS========
#########STAFF ADD########
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

#########STAFF REMOVE########
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

#########STAFF PROMOTE########
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

#########STAFF DEMOTE########
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

#########STAFF PANEL########
@staff_commands.command(
    name="panel",
    description="Send the staff panel"
)
async def panel(interaction: discord.Interaction):

    view = StaffPanel()

    message = await interaction.channel.send(
        "## Staff Panel\nClick below to interact.",
        view=view
    )

    db.insert_replace(
        "staff_panel",
        "guild_id, channel_id, message_id, enabled",
        (interaction.guild.id, interaction.channel.id, message.id, 1)
    )

    await interaction.response.send_message(
        "Staff panel created!",
        ephemeral=True
    )

#########STAFF APPLICATION#########
@staff_commands.command(
    name="application",
    description="Enable or disable the staff panel button"
)
@app_commands.choices(
    state=[
        app_commands.Choice(name="On", value="on"),
        app_commands.Choice(name="Off", value="off")
    ]
)
async def application(
    interaction: discord.Interaction,
    state: app_commands.Choice[str]
):

    data = db.fetchone(
        "staff_panel",
        "guild_id = ?",
        (interaction.guild.id,)
    )

    if not data:
        await interaction.response.send_message(
            "No staff panel has been created yet."
        )
        return

    enabled = state.value == "on"

    channel = interaction.guild.get_channel(data[1])

    if not channel:
        await interaction.response.send_message(
            "The staff panel channel no longer exists."
        )
        return

    try:
        message = await channel.fetch_message(data[2])

        embed = discord.Embed(
            title=(
                "OPENED"
                if enabled
                else "CLOSED"
            ),
            description=(
                "Click below to join our staff team of our Community!"
                if enabled 
                else "Our Community isn't in need for more staff members at the moment."
            ),
            color=(
                discord.Color.green()
                if enabled
                else discord.Color.red()
            )
        )

        await message.edit(
            embed=embed,
            view=StaffPanel(enabled=enabled)
        )

        db.update(
            "staff_panel",
            "enabled = ?",
            "guild_id = ?",
            (int(enabled), interaction.guild.id)
        )

        await interaction.response.send_message(
            f"Staff button is now **{'ON' if enabled else 'OFF'}**."
        )

    except discord.NotFound:
        await interaction.response.send_message(
            "The staff panel message no longer exists."
        )


def setup(bot):
    bot.tree.add_command(staff_commands)
    bot.add_view(StaffPanel())