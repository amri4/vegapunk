import asyncio
import discord
from discord import app_commands
from discord.ext import commands
import mycord
import time


# =========================================================
# DATABASE
# =========================================================

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

# Owner roles are stored separately from normal staff ranks.
db.create_table(
    "owner_roles",
    """
    guild_id INTEGER PRIMARY KEY,
    role_id INTEGER
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

def get_rank(member: discord.Member):

    result = db.fetchone(
        "staff_members",
        "user_id = ? AND guild_id = ?",
        (member.id, member.guild.id)
    )

    if result:
        return result[2]

    return None


async def get_staff_role(guild: discord.Guild, rank: str):

    result = db.fetchone(
        "staff_roles",
        "guild_id = ? AND rank = ?",
        (guild.id, rank)
    )

    if result:

        role = guild.get_role(result[2])

        if role:
            return role

    role = await guild.create_role(
        name=rank,
        reason="Creating staff rank role"
    )

    db.insert_replace(
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


async def change_staff_rank(
    member: discord.Member,
    new_rank: str,
    added_by: int
):

    if new_rank not in STAFF_RANKS:
        raise ValueError("Invalid staff rank.")

    old_rank = get_rank(member)

    if old_rank:

        old_role_data = db.fetchone(
            "staff_roles",
            "guild_id = ? AND rank = ?",
            (member.guild.id, old_rank)
        )

        if old_role_data:

            old_role = member.guild.get_role(old_role_data[2])

            if old_role:
                await member.remove_roles(old_role)

    new_role = await get_staff_role(
        member.guild,
        new_rank
    )

    await member.add_roles(new_role)

    db.insert_replace(
        "staff_members",
        "user_id, guild_id, rank, joined_at, added_by",
        (
            member.id,
            member.guild.id,
            new_rank,
            int(time.time()),
            added_by
        )
    )


# =========================================================
# OWNER ROLE
# =========================================================

async def get_owner_role(guild: discord.Guild):

    result = db.fetchone(
        "owner_roles",
        "guild_id = ?",
        (guild.id,)
    )

    # Retrieve the role using its saved ID.
    if result:

        role = guild.get_role(result[1])

        if role:
            return role

    # The saved role no longer exists, so create a replacement.
    role = await guild.create_role(
        name="Owner",
        reason="Creating server owner role"
    )

    # Save the new role ID.
    db.insert_replace(
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

def get_application_lock(channel_id: int):

    if channel_id not in application_locks:
        application_locks[channel_id] = asyncio.Lock()

    return application_locks[channel_id]


def get_application(channel: discord.TextChannel):

    return db.fetchone(
        "staff_applications",
        "channel_id = ? AND guild_id = ?",
        (channel.id, channel.guild.id)
    )


async def close_application_channel(
    channel: discord.TextChannel
):

    overwrites = {}

    for target, overwrite in channel.overwrites.items():

        if target.id == channel.guild.me.id:
            continue

        overwrite.send_messages = False
        overwrites[target] = overwrite

    await channel.edit(
        overwrites={
            **channel.overwrites,
            **overwrites
        }
    )


async def claim_reviewer(
    channel: discord.TextChannel,
    member: discord.Member
):

    async with get_application_lock(channel.id):

        application = get_application(channel)

        if not application:
            return False

        reviewer_id = application[3]
        status = application[4]

        if reviewer_id is not None:
            return False

        if status != "pending":
            return False

        if not get_rank(member):
            return False

        db.update(
            "staff_applications",
            "reviewer_id = ?, status = ?",
            "channel_id = ?",
            (member.id, "reviewing", channel.id)
        )

        try:

            applicant = channel.guild.get_member(
                application[2]
            )

            overwrites = {
                channel.guild.default_role: discord.PermissionOverwrite(
                    view_channel=False
                ),
                member: discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True
                )
            }

            if applicant:
                overwrites[applicant] = discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True
                )

            bot_member = channel.guild.me

            overwrites[bot_member] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                manage_channels=True
            )

            await channel.edit(
                overwrites=overwrites,
                topic=f"Application reviewer: {member.id}"
            )

        except discord.HTTPException:

            db.update(
                "staff_applications",
                "reviewer_id = ?, status = ?",
                "channel_id = ?",
                (None, "pending", channel.id)
            )

            raise

        await channel.send(
            f"{member.mention} has taken responsibility for this application."
        )

        return True


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

    if reviewer_id is None:

        if not get_rank(ctx.author):
            await ctx.reply("You are not a registered staff member.")
            return None

        claimed = await claim_reviewer(
            ctx.channel,
            ctx.author
        )

        if not claimed:
            await ctx.reply("This application has already been claimed.")
            return None

        return application

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
# STAFF APPLICATION PANEL
# =========================================================

class StaffPanel(discord.ui.View):

    def __init__(self, enabled=True):

        super().__init__(timeout=None)

        self.enabled = enabled

        self.join_button.label = (
            "Join Staff" if enabled else "Currently Closed"
        )

        self.join_button.style = (
            discord.ButtonStyle.success
            if enabled
            else discord.ButtonStyle.danger
        )

        self.join_button.emoji = (
            "➕" if enabled else "⛔"
        )

        self.join_button.disabled = not enabled

    @discord.ui.button(
        label="Join Staff",
        style=discord.ButtonStyle.success,
        emoji="➕",
        custom_id="staff:join"
    )
    async def join_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        guild = interaction.guild
        member = interaction.user

        panel = db.fetchone(
            "staff_panel",
            "guild_id = ?",
            (guild.id,)
        )

        if not panel or not panel[3]:

            await interaction.response.send_message(
                "Staff applications are currently closed.",
                ephemeral=True
            )
            return

        if get_rank(member):

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

        category = interaction.channel.category

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                view_channel=False
            ),
            member: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            ),
            guild.me: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                manage_channels=True
            )
        }

        staff_roles = get_registered_staff_roles(guild)

        for role in staff_roles:

            overwrites[role] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            )

        channel = await guild.create_text_channel(
            name=f"application-{member.name}",
            category=category,
            overwrites=overwrites,
            topic=f"Staff application by {member.id}"
        )

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

        mentions = " ".join(
            role.mention for role in staff_roles
        )

        await channel.send(
            f"{member.mention} welcome!\n"
            f"{mentions}\n\n"
            "A staff member will review your application when available."
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

    if not get_rank(message.author):
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
        title="Staff Application Commands",
        description=(
            "`help` - Show this help message\n"
            "`Confirm` - Accept the applicant\n"
            "`Close` - Close the application\n"
            "`Invite @member/@role` - Give someone access"
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
        await ctx.reply("This application is no longer active.")
        return

    guild = ctx.guild

    applicant = guild.get_member(application[2])

    if applicant is None:

        await ctx.reply("The applicant is no longer in this server.")
        return

    if get_rank(applicant):

        await ctx.reply("This member is already staff.")
        return

    role = await get_staff_role(
        guild,
        "Support Team"
    )

    await applicant.add_roles(
        role,
        reason=f"Staff application accepted by {ctx.author}"
    )

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
        f"Congratulations {applicant.mention}! Your application has been accepted."
    )

    await close_application_channel(ctx.channel)


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

    await ctx.send("This application has been closed.")

    await close_application_channel(ctx.channel)


@commands.command(name="Invite")
async def invite_application(
    ctx,
    target: discord.Member | discord.Role
):

    application = await require_reviewer(ctx)

    if not application:
        return

    if isinstance(target, discord.Member):

        if not get_rank(target):

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

    await ctx.channel.set_permissions(
        target,
        view_channel=True,
        send_messages=True,
        read_message_history=True
    )

    await ctx.send(
        f"{target.mention} has been invited to this application."
    )


# =========================================================
# STAFF SLASH COMMANDS
# =========================================================

staff_commands = app_commands.Group(
    name="staff",
    description="Community staff management"
)


@staff_commands.command(
    name="add",
    description="Add a member to the staff team"
)
@app_commands.describe(
    member="The member to add",
    rank="The staff rank"
)
@app_commands.choices(
    rank=[
        app_commands.Choice(name=rank, value=rank)
        for rank in STAFF_RANKS
    ]
)
async def staff_add(
    interaction: discord.Interaction,
    member: discord.Member,
    rank: app_commands.Choice[str]
):

    if not interaction.user.guild_permissions.administrator:

        await interaction.response.send_message(
            "You need administrator permissions.",
            ephemeral=True
        )
        return

    if get_rank(member):

        await interaction.response.send_message(
            "This member is already staff.",
            ephemeral=True
        )
        return

    await change_staff_rank(
        member,
        rank.value,
        interaction.user.id
    )

    await interaction.response.send_message(
        f"{member.mention} has been added as **{rank.value}**."
    )


@staff_commands.command(
    name="remove",
    description="Remove a member from the staff team"
)
async def staff_remove(
    interaction: discord.Interaction,
    member: discord.Member
):

    if not interaction.user.guild_permissions.administrator:

        await interaction.response.send_message(
            "You need administrator permissions.",
            ephemeral=True
        )
        return

    current_rank = get_rank(member)

    if not current_rank:

        await interaction.response.send_message(
            "This member is not staff.",
            ephemeral=True
        )
        return

    role_data = db.fetchone(
        "staff_roles",
        "guild_id = ? AND rank = ?",
        (interaction.guild.id, current_rank)
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
        f"{member.mention} has been removed from the staff team."
    )


@staff_commands.command(
    name="promote",
    description="Promote a staff member"
)
async def staff_promote(
    interaction: discord.Interaction,
    member: discord.Member
):

    if not interaction.user.guild_permissions.administrator:

        await interaction.response.send_message(
            "You need administrator permissions.",
            ephemeral=True
        )
        return

    current_rank = get_rank(member)

    if not current_rank:

        await interaction.response.send_message(
            "This member is not staff.",
            ephemeral=True
        )
        return

    current_level = STAFF_RANKS[current_rank]

    next_rank = next(
        (
            rank for rank, level in STAFF_RANKS.items()
            if level == current_level + 1
        ),
        None
    )

    if not next_rank:

        await interaction.response.send_message(
            "This member is already at the highest staff rank.",
            ephemeral=True
        )
        return

    await change_staff_rank(
        member,
        next_rank,
        interaction.user.id
    )

    await interaction.response.send_message(
        f"{member.mention} has been promoted to **{next_rank}**."
    )


@staff_commands.command(
    name="demote",
    description="Demote a staff member"
)
async def staff_demote(
    interaction: discord.Interaction,
    member: discord.Member
):

    if not interaction.user.guild_permissions.administrator:

        await interaction.response.send_message(
            "You need administrator permissions.",
            ephemeral=True
        )
        return

    current_rank = get_rank(member)

    if not current_rank:

        await interaction.response.send_message(
            "This member is not staff.",
            ephemeral=True
        )
        return

    current_level = STAFF_RANKS[current_rank]

    next_rank = next(
        (
            rank for rank, level in STAFF_RANKS.items()
            if level == current_level - 1
        ),
        None
    )

    if not next_rank:

        await interaction.response.send_message(
            "This member is already at the lowest staff rank.",
            ephemeral=True
        )
        return

    await change_staff_rank(
        member,
        next_rank,
        interaction.user.id
    )

    await interaction.response.send_message(
        f"{member.mention} has been demoted to **{next_rank}**."
    )


# =========================================================
# STAFF PANEL COMMAND
# =========================================================

@staff_commands.command(
    name="panel",
    description="Create the staff application panel"
)
async def staff_panel(
    interaction: discord.Interaction,
    channel: discord.TextChannel
):

    if not interaction.user.guild_permissions.administrator:

        await interaction.response.send_message(
            "You need administrator permissions.",
            ephemeral=True
        )
        return

    embed = discord.Embed(
        title="Join Our Staff Team",
        description=(
            "Interested in becoming part of our staff team?\n"
            "Click the button below to open a staff application."
        ),
        color=discord.Color.blue()
    )

    message = await channel.send(
        embed=embed,
        view=StaffPanel(enabled=True)
    )

    db.insert_replace(
        "staff_panel",
        "guild_id, channel_id, message_id, enabled",
        (
            interaction.guild.id,
            channel.id,
            message.id,
            1
        )
    )

    await interaction.response.send_message(
        f"Staff panel created in {channel.mention}.",
        ephemeral=True
    )


# =========================================================
# APPLICATION TOGGLE COMMANDS
# =========================================================

application_group = app_commands.Group(
    name="application",
    description="Manage staff applications",
    parent=staff_commands
)


async def set_application_status(
    interaction: discord.Interaction,
    enabled: bool
):

    if not interaction.user.guild_permissions.administrator:

        await interaction.response.send_message(
            "You need administrator permissions.",
            ephemeral=True
        )
        return

    panel = db.fetchone(
        "staff_panel",
        "guild_id = ?",
        (interaction.guild.id,)
    )

    if not panel:

        await interaction.response.send_message(
            "There is no staff panel configured.",
            ephemeral=True
        )
        return

    channel = interaction.guild.get_channel(panel[1])

    if not channel:

        await interaction.response.send_message(
            "The staff panel channel could not be found.",
            ephemeral=True
        )
        return

    try:

        message = await channel.fetch_message(panel[2])

        await message.edit(
            view=StaffPanel(enabled=enabled)
        )

    except discord.NotFound:

        await interaction.response.send_message(
            "The staff panel message no longer exists.",
            ephemeral=True
        )
        return

    db.update(
        "staff_panel",
        "enabled = ?",
        "guild_id = ?",
        (int(enabled), interaction.guild.id)
    )

    status = "opened" if enabled else "closed"

    await interaction.response.send_message(
        f"Staff applications have been **{status}**.",
        ephemeral=True
    )


@application_group.command(
    name="on",
    description="Open staff applications"
)
async def application_on(
    interaction: discord.Interaction
):

    await set_application_status(
        interaction,
        True
    )


@application_group.command(
    name="off",
    description="Close staff applications"
)
async def application_off(
    interaction: discord.Interaction
):

    await set_application_status(
        interaction,
        False
    )


# =========================================================
# SETUP
# =========================================================

def setup(bot):

    bot.tree.add_command(staff_commands)

    bot.add_view(StaffPanel())

    bot.add_listener(
        application_message_listener,
        "on_message"
    )

    # Register application prefix commands.
    # Remove the default help command to avoid a name conflict.
    bot.remove_command("help")

    bot.add_command(application_help)
    bot.add_command(confirm_application)
    bot.add_command(close_application)
    bot.add_command(invite_application)

    # on_ready receives no arguments, so use a closure.
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