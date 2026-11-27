
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
import mycord
import time
import asyncio


db = mycord.DB()


# =========================================================
# TABLES
# =========================================================

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

db.create_table(
    "owner_roles",
    """
    guild_id INTEGER PRIMARY KEY,
    role_id INTEGER
    """
)

db.create_table(
    "staff_applications",
    """
    channel_id INTEGER PRIMARY KEY,
    guild_id INTEGER,
    user_id INTEGER,
    reviewer_id INTEGER,
    status TEXT,
    created_at INTEGER
    """
)


# =========================================================
# CONFIGURATION
# =========================================================

STAFF_RANKS = {
    "Head Administrator": 5,
    "Administrator": 4,
    "Senior Moderator": 3,
    "Moderator": 2,
    "Support Team": 1
}

application_locks = {}


# =========================================================
# STAFF FUNCTIONS
# =========================================================

def get_rank(member: discord.Member, guild: discord.Guild):

    staff = db.fetchone(
        "staff_members",
        "user_id = ? AND guild_id = ?",
        (member.id, guild.id)
    )

    if not staff:
        return None

    return staff[2]


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

        db.delete(
            "staff_roles",
            "guild_id = ? AND rank = ?",
            (guild.id, rank)
        )

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


def get_registered_staff_roles(guild: discord.Guild):

    rows = db.fetchall("staff_roles")

    roles = []

    for row in rows:

        if row[0] != guild.id:
            continue

        role = guild.get_role(row[2])

        if role:
            roles.append(role)

    return roles


async def change_staff_rank(interaction, member, direction):

    guild = interaction.guild

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

        old_role = await get_staff_role(guild, current_rank)
        new_role = await get_staff_role(guild, new_rank)

        await member.add_roles(new_role)
        await member.remove_roles(old_role)

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


# =========================================================
# OWNER ROLE
# =========================================================

async def get_owner_role(guild: discord.Guild):

    role_data = db.fetchone(
        "owner_roles",
        "guild_id = ?",
        (guild.id,)
    )

    if role_data:

        role = guild.get_role(role_data[1])

        if role:
            return role

        db.delete(
            "owner_roles",
            "guild_id = ?",
            (guild.id,)
        )

    role = await guild.create_role(
        name="Owner",
        reason="Creating server owner role"
    )

    db.insert(
        "owner_roles",
        "guild_id, role_id",
        (guild.id, role.id)
    )

    return role


async def assign_owner_role(guild: discord.Guild):

    owner = guild.owner

    if owner is None:
        owner = await guild.fetch_member(guild.owner_id)

    role = await get_owner_role(guild)

    if role not in owner.roles:

        await owner.add_roles(
            role,
            reason="Automatically assigning server owner role"
        )


# =========================================================
# APPLICATION FUNCTIONS
# =========================================================

def get_application(channel: discord.TextChannel):

    return db.fetchone(
        "staff_applications",
        "channel_id = ? AND guild_id = ?",
        (channel.id, channel.guild.id)
    )


def get_application_lock(channel_id: int):

    if channel_id not in application_locks:
        application_locks[channel_id] = asyncio.Lock()

    return application_locks[channel_id]


async def claim_reviewer(
    channel: discord.TextChannel,
    member: discord.Member
):

    async with get_application_lock(channel.id):

        application = get_application(channel)

        if not application:
            return False

        if application[3] is not None:
            return False

        if application[4] != "pending":
            return False

        if not get_rank(member, channel.guild):
            return False

        applicant = channel.guild.get_member(application[2])

        if applicant is None:
            return False

        # Build new permissions.
        overwrites = {
            channel.guild.default_role:
                discord.PermissionOverwrite(
                    view_channel=False
                ),

            applicant:
                discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True
                ),

            member:
                discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True
                ),

            channel.guild.me:
                discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True,
                    manage_channels=True
                )
        }

        # Explicitly remove access from all staff roles.
        # The reviewer receives their own member overwrite.
        for role in get_registered_staff_roles(channel.guild):

            overwrites[role] = discord.PermissionOverwrite(
                view_channel=False
            )

        try:

            await channel.edit(
                overwrites=overwrites,
                topic=f"Application reviewer: {member.id}"
            )

        except discord.HTTPException:
            return False

        db.update(
            "staff_applications",
            "reviewer_id = ?, status = ?",
            "channel_id = ?",
            (member.id, "reviewing", channel.id)
        )

        await channel.send(
            f"{member.mention} has been assigned as this application's reviewer."
        )

        return True


async def close_application_channel(channel: discord.TextChannel):

    overwrites = dict(channel.overwrites)

    for target, overwrite in overwrites.items():

        if target == channel.guild.me:
            continue

        overwrite.send_messages = False
        overwrites[target] = overwrite

    await channel.edit(overwrites=overwrites)


async def require_application(ctx):

    if not ctx.guild:
        return None

    application = get_application(ctx.channel)

    if not application:

        await ctx.reply(
            "This command can only be used in an application channel."
        )

        return None

    return application


async def require_reviewer(ctx):

    application = await require_application(ctx)

    if not application:
        return None

    reviewer_id = application[3]

    # No reviewer yet: first registered staff member
    # using a command can claim the application.
    if reviewer_id is None:

        if not get_rank(ctx.author, ctx.guild):

            await ctx.reply(
                "You are not a registered staff member."
            )

            return None

        claimed = await claim_reviewer(
            ctx.channel,
            ctx.author
        )

        if not claimed:

            await ctx.reply(
                "This application could not be claimed."
            )

            return None

        return get_application(ctx.channel)

    # Reviewer or server administrator.
    if (
        ctx.author.id != reviewer_id
        and not ctx.author.guild_permissions.administrator
    ):

        await ctx.reply(
            "Only the assigned reviewer can use this command."
        )

        return None

    return application


# =========================================================
# STAFF PANEL VIEW
# =========================================================

class StaffPanel(discord.ui.View):

    def __init__(self, enabled=True):

        super().__init__(timeout=None)

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

        guild = interaction.guild
        member = interaction.user

        panel_data = db.fetchone(
            "staff_panel",
            "guild_id = ?",
            (guild.id,)
        )

        if not panel_data or not panel_data[3]:

            await interaction.response.send_message(
                "Staff applications are currently closed.",
                ephemeral=True
            )
            return

        if get_rank(member, guild):

            await interaction.response.send_message(
                "You are already a staff member.",
                ephemeral=True
            )
            return

        existing = db.fetchone(
            "staff_applications",
            "guild_id = ? AND user_id = ? AND status IN ('pending', 'reviewing')",
            (guild.id, member.id)
        )

        if existing:

            existing_channel = guild.get_channel(existing[0])

            if existing_channel:

                await interaction.response.send_message(
                    f"You already have an application: {existing_channel.mention}",
                    ephemeral=True
                )

            else:

                await interaction.response.send_message(
                    "You already have an open application.",
                    ephemeral=True
                )

            return

        staff_roles = get_registered_staff_roles(guild)

        overwrites = {
            guild.default_role:
                discord.PermissionOverwrite(
                    view_channel=False
                ),

            member:
                discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True
                ),

            guild.me:
                discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True,
                    manage_channels=True
                )
        }

        for role in staff_roles:

            overwrites[role] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            )

        try:

            channel = await guild.create_text_channel(
                name=f"application-{member.name}",
                category=interaction.channel.category,
                overwrites=overwrites,
                topic=f"Staff application by {member.id}"
            )

        except discord.HTTPException:

            await interaction.response.send_message(
                "I couldn't create your application channel. "
                "Check my channel permissions.",
                ephemeral=True
            )

            return

        db.insert(
            "staff_applications",
            "channel_id, guild_id, user_id, reviewer_id, status, created_at",
            (
                channel.id,
                guild.id,
                member.id,
                None,
                "pending",
                int(time.time())
            )
        )

        role_mentions = " ".join(
            role.mention for role in staff_roles
        )

        await channel.send(
            f"{member.mention} welcome to your staff application!\n"
            f"{role_mentions}\n\n"
            "A staff member will review your application when available.",
            allowed_mentions=discord.AllowedMentions(
                users=True,
                roles=True
            )
        )

        await interaction.response.send_message(
            f"Your application channel has been created: {channel.mention}",
            ephemeral=True
        )


# =========================================================
# APPLICATION MESSAGE LISTENER
# =========================================================

async def application_message_listener(message: discord.Message):

    if message.author.bot or not message.guild:
        return

    application = get_application(message.channel)

    if not application:
        return

    if application[3] is not None:
        return

    if application[4] != "pending":
        return

    if not get_rank(message.author, message.guild):
        return

    await claim_reviewer(
        message.channel,
        message.author
    )


# =========================================================
# APPLICATION PREFIX COMMANDS
# =========================================================

@commands.command(name="help")
async def application_help(ctx):

    application = await require_application(ctx)

    if not application:
        return

    embed = discord.Embed(
        title="Application Commands",
        description=(
            "`help` - Show application commands\n"
            "`Confirm` - Accept the applicant\n"
            "`Close` - Close the application\n"
            "`Invite @member/@role` - Invite staff"
        ),
        color=discord.Color.blue()
    )

    await ctx.reply(embed=embed)


@commands.command(name="Confirm")
async def confirm_application(ctx):

    application = await require_reviewer(ctx)

    if not application:
        return

    if application[4] not in ("pending", "reviewing"):

        await ctx.reply(
            "This application is no longer active."
        )
        return

    guild = ctx.guild

    applicant = guild.get_member(application[2])

    if applicant is None:

        await ctx.reply(
            "The applicant is no longer in this server."
        )
        return

    if get_rank(applicant, guild):

        await ctx.reply(
            "This member is already a staff member."
        )
        return

    role = await get_staff_role(
        guild,
        "Support Team"
    )

    try:

        await applicant.add_roles(
            role,
            reason=f"Application accepted by {ctx.author}"
        )

    except discord.HTTPException:

        await ctx.reply(
            "I couldn't assign the Support Team role."
        )
        return

    db.insert_replace(
        "staff_members",
        "user_id, guild_id, rank, joined_at, added_by",
        (
            applicant.id,
            guild.id,
            "Support Team",
            int(time.time()),
            ctx.author.id
        )
    )

    db.update(
        "staff_applications",
        "status = ?",
        "channel_id = ?",
        ("accepted", ctx.channel.id)
    )

    await ctx.send(
        f"Congratulations {applicant.mention}! "
        "Your application has been accepted."
    )

    await close_application_channel(ctx.channel)
    await asyncio.sleep(120)
    await interaction.channel.delete()


@commands.command(name="Close")
async def close_application(ctx):

    application = await require_reviewer(ctx)

    if not application:
        return

    db.update(
        "staff_applications",
        "status = ?",
        "channel_id = ?",
        ("closed", ctx.channel.id)
    )

    await ctx.send(
        "This application has been closed, this channel will be deleted in 5 minuits."
    )

    await close_application_channel(ctx.channel)
    await asyncio.sleep(300)
    await interaction.channel.delete()


@commands.command(name="Invite")
async def invite_application(
    ctx,
    target: discord.Member | discord.Role
):

    application = await require_reviewer(ctx)

    if not application:
        return

    if application[4] not in ("pending", "reviewing"):

        await ctx.reply(
            "This application is no longer active."
        )
        return

    if isinstance(target, discord.Member):

        if not get_rank(target, ctx.guild):

            await ctx.reply(
                "You can only invite registered staff members."
            )
            return

    elif isinstance(target, discord.Role):

        staff_roles = get_registered_staff_roles(ctx.guild)

        if target not in staff_roles:

            await ctx.reply(
                "You can only invite registered staff roles."
            )
            return

    try:

        await ctx.channel.set_permissions(
            target,
            view_channel=True,
            send_messages=True,
            read_message_history=True
        )

    except discord.HTTPException:

        await ctx.reply(
            "I couldn't give this member or role access."
        )
        return

    await ctx.send(
        f"{target.mention} has been invited to this application."
    )


# =========================================================
# SLASH COMMAND GROUP
# =========================================================

staff_commands = app_commands.Group(
    name="staff",
    description="Community staff management"
)


# ---------------- STAFF ADD ----------------

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

    role = await get_staff_role(
        interaction.guild,
        st_rank
    )

    try:

        await member.add_roles(role)

    except discord.HTTPException:

        await interaction.response.send_message(
            "I couldn't assign the staff role."
        )
        return

    actor = interaction.user

    db.insert(
        "staff_members",
        "user_id, guild_id, rank, joined_at, added_by",
        (
            member.id,
            interaction.guild.id,
            st_rank,
            int(time.time()),
            actor.id
        )
    )

    rank = get_rank(member, interaction.guild)

    await interaction.response.send_message(
        f"{member.mention} has been added by "
        f"{actor.mention} as a **{rank}** staff member."
    )


# ---------------- STAFF REMOVE ----------------

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

            try:
                await member.remove_roles(role)

            except discord.HTTPException:

                await interaction.response.send_message(
                    "I couldn't remove the Discord role."
                )
                return

    db.delete(
        "staff_members",
        "user_id = ? AND guild_id = ?",
        (member.id, interaction.guild.id)
    )

    await interaction.response.send_message(
        f"{member.mention} is no longer a staff member."
    )


# ---------------- STAFF PROMOTE ----------------

@staff_commands.command(
    name="promote",
    description="Promote a staff member"
)
async def promote(
    interaction: discord.Interaction,
    member: discord.Member
):

    await change_staff_rank(
        interaction,
        member,
        1
    )


# ---------------- STAFF DEMOTE ----------------

@staff_commands.command(
    name="demote",
    description="Demote a staff member"
)
async def demote(
    interaction: discord.Interaction,
    member: discord.Member
):

    await change_staff_rank(
        interaction,
        member,
        -1
    )


# ---------------- STAFF PANEL ----------------

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
        (
            interaction.guild.id,
            interaction.channel.id,
            message.id,
            1
        )
    )

    await interaction.response.send_message(
        "Staff panel created!",
        ephemeral=True
    )


# ---------------- STAFF APPLICATION ----------------

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
            title="OPENED" if enabled else "CLOSED",
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


# =========================================================
# SETUP
# =========================================================

def setup(bot):

    bot.tree.add_command(staff_commands)

    bot.add_view(StaffPanel())

    # The custom application help command uses "help".
    # Remove discord.py's default help command to avoid conflict.
    bot.remove_command("help")

    bot.add_command(application_help)
    bot.add_command(confirm_application)
    bot.add_command(close_application)
    bot.add_command(invite_application)

    bot.add_listener(
        application_message_listener,
        "on_message"
    )

    # Owner role assignment.
    # on_ready does not receive a bot argument, so use a closure.

    async def assign_all_owner_roles():

        for guild in bot.guilds:

            try:
                await assign_owner_role(guild)

            except discord.HTTPException as error:

                print(
                    f"OWNER ROLE ERROR ({guild.id}): {error}",
                    flush=True
                )

    async def owner_joined_guild(guild):

        try:
            await assign_owner_role(guild)

        except discord.HTTPException as error:

            print(
                f"OWNER ROLE ERROR ({guild.id}): {error}",
                flush=True
            )

    bot.add_listener(
        assign_all_owner_roles,
        "on_ready"
    )

    bot.add_listener(
        owner_joined_guild,
        "on_guild_join"
    )
