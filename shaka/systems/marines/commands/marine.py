import discord
from discord import app_commands
import mycord

from shaka.systems.bounty.functions.set_bounty import set_bounty
from shaka.systems.marines.functions.honor import MARINE_RANKS
from york.systems.berries.functions.berries import get_berries, remove_berries

db = mycord.DB()

db.create_table(
    "marines",
    """
    guild_id INTEGER,
    user_id INTEGER,
    rank INTEGER DEFAULT 2,
    honor INTEGER DEFAULT 0
    """
)

# Traitor bounty when a Marine deserts to become a Pirate (scaled by rank)
DESERTION_BOUNTIES = {
    0: 0,           # Chore-Boy
    1: 0,           # Trainee
    2: 50_000,      # Recruit
    3: 250_000,     # Lieutenant
    4: 1_000_000,   # Captain
    5: 5_000_000,   # Vice Admiral
    6: 15_000_000,  # Admiral
    7: 30_000_000,  # Fleet Admiral
}


def has_role(member: discord.Member, role_name: str) -> bool:
    return any(r.name == role_name for r in member.roles)


def get_or_create_marine(guild_id: int, user_id: int, default_rank: int = 2):
    row = db.fetchone("marines", "guild_id = ? AND user_id = ?", (guild_id, user_id))
    if row is None:
        db.insert("marines", "guild_id, user_id, rank, honor", (guild_id, user_id, default_rank, 0))
        return default_rank, 0
    return row[2], row[3]


def set_marine_data(guild_id: int, user_id: int, rank: int, honor: int = None):
    row = db.fetchone("marines", "guild_id = ? AND user_id = ?", (guild_id, user_id))
    if row is not None:
        new_honor = row[3] if honor is None else honor
        db.update(
            "marines",
            "rank = ?, honor = ?",
            "guild_id = ? AND user_id = ?",
            (rank, new_honor, guild_id, user_id)
        )
    else:
        db.insert(
            "marines",
            "guild_id, user_id, rank, honor",
            (guild_id, user_id, rank, 0 if honor is None else honor)
        )


def is_fleet_admiral_or_admin(member: discord.Member) -> bool:
    if member.guild_permissions.administrator:
        return True
    if not has_role(member, "Marine"):
        return False
    rank, _ = get_or_create_marine(member.guild.id, member.id)
    return rank == 7


class DefectConfirmView(discord.ui.View):
    """Pirate -> Marine (starts at Chore-Boy, loses crew & bounty)"""
    def __init__(self, user_id: int):
        super().__init__(timeout=60)
        self.user_id = user_id

    @discord.ui.button(label="Confirm Defection", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This confirmation isn't for you.", ephemeral=True)
            return

        await interaction.response.defer()

        guild = interaction.guild
        member = interaction.user
        pirate_role = discord.utils.get(guild.roles, name="Pirate")
        marine_role = discord.utils.get(guild.roles, name="Marine")

        if marine_role is None:
            await interaction.edit_original_response(content="❌ The **Marine** role doesn't exist.", view=None)
            return

        try:
            if pirate_role and pirate_role in member.roles:
                await member.remove_roles(pirate_role, reason="Defected to Marines")
            await member.add_roles(marine_role, reason="Defected to Marines")
        except discord.Forbidden:
            await interaction.edit_original_response(
                content="❌ I don't have permission to swap your roles.",
                view=None
            )
            return

        # Wipe crew membership (disband if Captain)
        membership = db.fetchone("crew_members", "guild_id = ? AND user_id = ?", (guild.id, member.id))
        if membership:
            crew_name = membership[2]
            crew = db.fetchone("crews", "guild_id = ? AND name = ?", (guild.id, crew_name))
            if crew and crew[2] == member.id:
                db.delete("crew_members", "guild_id = ? AND crew_name = ?", (guild.id, crew_name))
                db.delete("crews", "guild_id = ? AND name = ?", (guild.id, crew_name))
            else:
                db.delete("crew_members", "guild_id = ? AND user_id = ?", (guild.id, member.id))

        set_bounty(guild.id, member.id, 0)
        set_marine_data(guild.id, member.id, rank=0, honor=0)

        self.stop()
        await interaction.edit_original_response(
            content=(
                f"⚓ {member.mention} abandoned the Pirate life! "
                "Your crew and bounty have been wiped, and you now start at the bottom as a **Chore-Boy**."
            ),
            view=None
        )

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This confirmation isn't for you.", ephemeral=True)
            return
        self.stop()
        await interaction.response.edit_message(content="Defection cancelled. You remain a Pirate.", view=None)


class DesertConfirmView(discord.ui.View):
    """Marine -> Pirate (loses 50% berries, rank wiped, gets traitor bounty)"""
    def __init__(self, user_id: int):
        super().__init__(timeout=60)
        self.user_id = user_id

    @discord.ui.button(label="Confirm Desertion", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This confirmation isn't for you.", ephemeral=True)
            return

        await interaction.response.defer()

        guild = interaction.guild
        member = interaction.user
        pirate_role = discord.utils.get(guild.roles, name="Pirate")
        marine_role = discord.utils.get(guild.roles, name="Marine")

        if pirate_role is None:
            await interaction.edit_original_response(content="❌ The **Pirate** role doesn't exist.", view=None)
            return

        rank_idx, _ = get_or_create_marine(guild.id, member.id)

        try:
            if marine_role and marine_role in member.roles:
                await member.remove_roles(marine_role, reason="Deserted to Pirates")
            await member.add_roles(pirate_role, reason="Deserted to Pirates")
        except discord.Forbidden:
            await interaction.edit_original_response(
                content="❌ I don't have permission to swap your roles.",
                view=None
            )
            return

        # Seize 50% of berries (safe fallback if York's berries table isn't initialized yet)
        try:
            current_berries = get_berries(guild.id, member.id)
            seized = current_berries // 2
            if seized > 0:
                remove_berries(guild.id, member.id, seized)
        except Exception:
            seized = 0

        # Remove Marine record & place traitor bounty
        db.delete("marines", "guild_id = ? AND user_id = ?", (guild.id, member.id))
        traitor_bounty = DESERTION_BOUNTIES.get(rank_idx, 50_000)
        set_bounty(guild.id, member.id, traitor_bounty)

        self.stop()
        await interaction.edit_original_response(
            content=(
                f"🏴‍☠️ {member.mention} deserted the Marines as a **{MARINE_RANKS[rank_idx]}**!\n"
                f"• The World Government seized **{seized:,} Berries** (50%).\n"
                f"• A traitor bounty of **฿{traitor_bounty:,}** has been placed on your head."
            ),
            view=None
        )

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This confirmation isn't for you.", ephemeral=True)
            return
        self.stop()
        await interaction.response.edit_message(content="Desertion cancelled. You remain a Marine.", view=None)


marine_group = app_commands.Group(name="marine", description="Manage the Marine Fleet and ranks.")


@marine_group.command(name="profile", description="View a Marine's rank and Honor.")
async def marine_profile(interaction: discord.Interaction, member: discord.Member = None):
    target = member or interaction.user

    if not has_role(target, "Marine"):
        await interaction.response.send_message(f"❌ {target.mention} is not a Marine.", ephemeral=True)
        return

    rank_idx, honor = get_or_create_marine(interaction.guild.id, target.id)
    embed = discord.Embed(
        title=f"⚓ Marine Profile — {target.display_name}",
        description=(
            f"**Rank:** {MARINE_RANKS[rank_idx]}\n"
            f"**Honor:** {honor:,}\n"
            f"**Authority Level:** {rank_idx} / {len(MARINE_RANKS) - 1}"
        ),
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed)


@marine_group.command(name="roster", description="View the Marine Fleet sorted by rank.")
async def marine_roster(interaction: discord.Interaction):
    all_rows = db.fetchall("marines")
    rows = [r for r in all_rows if r[0] == interaction.guild.id]

    active_marines = []
    for row in rows:
        uid, rank_idx, honor = row[1], row[2], row[3]
        member = interaction.guild.get_member(uid)
        if member and has_role(member, "Marine"):
            active_marines.append((rank_idx, honor, member))

    if not active_marines:
        await interaction.response.send_message("⚓ No Marines are registered in the fleet yet.", ephemeral=True)
        return

    active_marines.sort(key=lambda item: (item[0], item[1]), reverse=True)

    lines = [
        f"**{MARINE_RANKS[rank_idx]}** — {member.mention} ({honor:,} Honor)"
        for rank_idx, honor, member in active_marines
    ]

    embed = discord.Embed(
        title="⚓ Marine Fleet Roster",
        description="\n".join(lines),
        color=discord.Color.blue()
    )
    embed.set_footer(text=f"Total Marines: {len(active_marines)}")
    await interaction.response.send_message(embed=embed)


@marine_group.command(name="promote", description="Promote a Marine (Fleet Admiral only).")
async def marine_promote(interaction: discord.Interaction, member: discord.Member):
    if not is_fleet_admiral_or_admin(interaction.user):
        await interaction.response.send_message("❌ Only the **Fleet Admiral** can manually promote Marines.", ephemeral=True)
        return

    if not has_role(member, "Marine"):
        await interaction.response.send_message(f"❌ {member.mention} is not a Marine.", ephemeral=True)
        return

    target_rank, _ = get_or_create_marine(interaction.guild.id, member.id)
    if target_rank >= len(MARINE_RANKS) - 1:
        await interaction.response.send_message(f"❌ {member.mention} is already **Fleet Admiral**.", ephemeral=True)
        return

    if target_rank + 1 == 7 and not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Only a Server Administrator can appoint a **Fleet Admiral**.", ephemeral=True)
        return

    new_rank = target_rank + 1
    set_marine_data(interaction.guild.id, member.id, new_rank)
    await interaction.response.send_message(f"🎖️ {member.mention} has been promoted to **{MARINE_RANKS[new_rank]}**!")


@marine_group.command(name="demote", description="Demote a Marine (Fleet Admiral only).")
async def marine_demote(interaction: discord.Interaction, member: discord.Member):
    if not is_fleet_admiral_or_admin(interaction.user):
        await interaction.response.send_message("❌ Only the **Fleet Admiral** can manually demote Marines.", ephemeral=True)
        return

    if not has_role(member, "Marine"):
        await interaction.response.send_message(f"❌ {member.mention} is not a Marine.", ephemeral=True)
        return

    target_rank, _ = get_or_create_marine(interaction.guild.id, member.id)
    if target_rank <= 0:
        await interaction.response.send_message(f"❌ {member.mention} is already at **Chore-Boy**.", ephemeral=True)
        return

    new_rank = target_rank - 1
    set_marine_data(interaction.guild.id, member.id, new_rank)
    await interaction.response.send_message(f"⬇️ {member.mention} has been demoted to **{MARINE_RANKS[new_rank]}**.")


@marine_group.command(name="defect", description="Abandon the Pirate life and restart as a Marine Chore-Boy.")
async def marine_defect(interaction: discord.Interaction):
    if not has_role(interaction.user, "Pirate"):
        await interaction.response.send_message("❌ Only Pirates can defect to the Marines.", ephemeral=True)
        return

    view = DefectConfirmView(interaction.user.id)
    await interaction.response.send_message(
        "⚠️ **Are you sure you want to defect to the Marines?**\n"
        "You will lose your **Pirate** role, your **crew**, and your **bounty** will be reset to `0`. "
        "You will start at the bottom as a **Chore-Boy**.",
        view=view,
        ephemeral=True
    )


@marine_group.command(name="desert", description="Leave the Marines and become a Pirate (50% Berries seized + traitor bounty).")
async def marine_desert(interaction: discord.Interaction):
    if not has_role(interaction.user, "Marine"):
        await interaction.response.send_message("❌ Only Marines can desert to the Pirates.", ephemeral=True)
        return

    rank_idx, _ = get_or_create_marine(interaction.guild.id, interaction.user.id)
    traitor_bounty = DESERTION_BOUNTIES.get(rank_idx, 50_000)

    view = DesertConfirmView(interaction.user.id)
    await interaction.response.send_message(
        f"⚠️ **Are you sure you want to desert the Marines?**\n"
        f"• You will lose your **{MARINE_RANKS[rank_idx]}** rank and **Marine** role.\n"
        f"• **50% of your Berries** will be seized by the World Government.\n"
        f"• A traitor bounty of **฿{traitor_bounty:,}** will be placed on your head.",
        view=view,
        ephemeral=True
    )


def setup(bot):
    bot.tree.add_command(marine_group)