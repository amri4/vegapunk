import discord
from discord import app_commands
import mycord
db = mycord.DB()

db.create_table(
    "crews",
    """
    guild_id INTEGER,
    name TEXT,
    captain_id INTEGER
    """
)

db.create_table(
    "crew_members",
    """
    guild_id INTEGER,
    user_id INTEGER,
    crew_name TEXT,
    title TEXT DEFAULT ''
    """
)

def has_role(member: discord.Member, role_name: str) -> bool:
    return any(r.name == role_name for r in member.roles)


def get_member_crew(guild_id: int, user_id: int):
    return db.fetchone(
        "crew_members",
        "guild_id = ? AND user_id = ?",
        (guild_id, user_id)
    )


class CrewInviteView(discord.ui.View):
    def __init__(self, guild_id: int, crew_name: str, target_id: int):
        super().__init__(timeout=120)
        self.guild_id = guild_id
        self.crew_name = crew_name
        self.target_id = target_id

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.success)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.target_id:
            await interaction.response.send_message("This invite isn't for you.", ephemeral=True)
            return

        if get_member_crew(self.guild_id, self.target_id):
            await interaction.response.send_message("You're already in a crew.", ephemeral=True)
            return

        db.insert(
            "crew_members",
            "guild_id, user_id, crew_name, title",
            (self.guild_id, self.target_id, self.crew_name, "")
        )

        self.stop()
        await interaction.response.edit_message(
            content=f"🏴‍☠️ {interaction.user.mention} joined **{self.crew_name}**!",
            view=None
        )

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.danger)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.target_id:
            await interaction.response.send_message("This invite isn't for you.", ephemeral=True)
            return

        self.stop()
        await interaction.response.edit_message(
            content=f"{interaction.user.mention} declined the invite to **{self.crew_name}**.",
            view=None
        )


crew_group = app_commands.Group(name="crew", description="Manage Pirate crews.")


@crew_group.command(name="create", description="Create a new Pirate crew.")
async def crew_create(interaction: discord.Interaction, name: str):
    try:
        if not has_role(interaction.user, "Pirate"):
            await interaction.response.send_message("❌ Only Pirates can form a crew.", ephemeral=True)
            return

        if get_member_crew(interaction.guild.id, interaction.user.id):
            await interaction.response.send_message("❌ You're already in a crew. Leave it first.", ephemeral=True)
            return

        if db.exists("crews", "guild_id = ? AND LOWER(name) = LOWER(?)", (interaction.guild.id, name)):
            await interaction.response.send_message(f"❌ A crew named **{name}** already exists.", ephemeral=True)
            return

        db.insert("crews", "guild_id, name, captain_id", (interaction.guild.id, name, interaction.user.id))
        db.insert("crew_members", "guild_id, user_id, crew_name, title", (interaction.guild.id, interaction.user.id, name, "Captain"))

        await interaction.response.send_message(f"🏴‍☠️ **{name}** has set sail! {interaction.user.mention} is the Captain.")
    except Exception as e:
        print(f"[CREW CREATE ERROR] {type(e).__name__}: {e}")
        await interaction.response.send_message(f"⚠️ Error: `{type(e).__name__}: {e}`", ephemeral=True)

@crew_group.command(name="info", description="View info about a Pirate crew.")
async def crew_info(interaction: discord.Interaction, name: str = None):
    if name is None:
        membership = get_member_crew(interaction.guild.id, interaction.user.id)
        if not membership:
            await interaction.response.send_message("❌ You aren't in a crew. Provide a crew name to look one up.", ephemeral=True)
            return
        name = membership[2]

    crew = db.fetchone("crews", "guild_id = ? AND LOWER(name) = LOWER(?)", (interaction.guild.id, name))
    if not crew:
        await interaction.response.send_message(f"❌ Crew **{name}** not found.", ephemeral=True)
        return

    crew_name, captain_id = crew[1], crew[2]
    all_members = db.fetchall("crew_members")
    members = [m for m in all_members if m[0] == interaction.guild.id and m[2] == crew_name]

    lines = []
    for m in members:
        uid, title = m[1], m[3]
        tag = f" — *{title}*" if title else ""
        lines.append(f"• <@{uid}>{tag}")

    embed = discord.Embed(
        title=f"🏴‍☠️ {crew_name}",
        description="\n".join(lines) if lines else "No members.",
        color=discord.Color.dark_red()
    )
    embed.set_footer(text=f"Members: {len(members)}")
    await interaction.response.send_message(embed=embed)


@crew_group.command(name="invite", description="Invite a Pirate to your crew (Captain only).")
async def crew_invite(interaction: discord.Interaction, member: discord.Member):
    if member.bot:
        await interaction.response.send_message("❌ You can't invite a bot.", ephemeral=True)
        return

    crew = db.fetchone("crews", "guild_id = ? AND captain_id = ?", (interaction.guild.id, interaction.user.id))
    if not crew:
        await interaction.response.send_message("❌ Only a crew Captain can invite members.", ephemeral=True)
        return

    if not has_role(member, "Pirate"):
        await interaction.response.send_message(f"❌ {member.mention} is not a Pirate.", ephemeral=True)
        return

    if get_member_crew(interaction.guild.id, member.id):
        await interaction.response.send_message(f"❌ {member.mention} is already in a crew.", ephemeral=True)
        return

    crew_name = crew[1]
    view = CrewInviteView(interaction.guild.id, crew_name, member.id)
    await interaction.response.send_message(
        f"{member.mention}, **{interaction.user.display_name}** invited you to join **{crew_name}**!",
        view=view
    )


@crew_group.command(name="kick", description="Remove a member from your crew (Captain only).")
async def crew_kick(interaction: discord.Interaction, member: discord.Member):
    crew = db.fetchone("crews", "guild_id = ? AND captain_id = ?", (interaction.guild.id, interaction.user.id))
    if not crew:
        await interaction.response.send_message("❌ Only a crew Captain can kick members.", ephemeral=True)
        return

    if member.id == interaction.user.id:
        await interaction.response.send_message("❌ Use `/crew leave` to disband your crew.", ephemeral=True)
        return

    crew_name = crew[1]
    target = db.fetchone("crew_members", "guild_id = ? AND user_id = ? AND crew_name = ?", (interaction.guild.id, member.id, crew_name))
    if not target:
        await interaction.response.send_message(f"❌ {member.mention} isn't in **{crew_name}**.", ephemeral=True)
        return

    db.delete("crew_members", "guild_id = ? AND user_id = ?", (interaction.guild.id, member.id))
    await interaction.response.send_message(f"👢 {member.mention} was kicked from **{crew_name}**.")


@crew_group.command(name="leave", description="Leave your current crew (disbands if you are Captain).")
async def crew_leave(interaction: discord.Interaction):
    membership = get_member_crew(interaction.guild.id, interaction.user.id)
    if not membership:
        await interaction.response.send_message("❌ You aren't in a crew.", ephemeral=True)
        return

    crew_name = membership[2]
    crew = db.fetchone("crews", "guild_id = ? AND name = ?", (interaction.guild.id, crew_name))

    if crew and crew[2] == interaction.user.id:
        db.delete("crew_members", "guild_id = ? AND crew_name = ?", (interaction.guild.id, crew_name))
        db.delete("crews", "guild_id = ? AND name = ?", (interaction.guild.id, crew_name))
        await interaction.response.send_message(f"💥 Captain {interaction.user.mention} left — **{crew_name}** has been disbanded.")
    else:
        db.delete("crew_members", "guild_id = ? AND user_id = ?", (interaction.guild.id, interaction.user.id))
        await interaction.response.send_message(f"👋 {interaction.user.mention} left **{crew_name}**.")


@crew_group.command(name="title", description="Set or clear a crew member's custom title (Captain only).")
async def crew_title(interaction: discord.Interaction, member: discord.Member, title: str = ""):
    crew = db.fetchone("crews", "guild_id = ? AND captain_id = ?", (interaction.guild.id, interaction.user.id))
    if not crew:
        await interaction.response.send_message("❌ Only a crew Captain can assign titles.", ephemeral=True)
        return

    crew_name = crew[1]
    target = db.fetchone("crew_members", "guild_id = ? AND user_id = ? AND crew_name = ?", (interaction.guild.id, member.id, crew_name))
    if not target:
        await interaction.response.send_message(f"❌ {member.mention} isn't in **{crew_name}**.", ephemeral=True)
        return

    db.update("crew_members", "title = ?", "guild_id = ? AND user_id = ?", (title.strip(), interaction.guild.id, member.id))
    if title.strip():
        await interaction.response.send_message(f"🏷️ {member.mention} is now **{title.strip()}** of **{crew_name}**.")
    else:
        await interaction.response.send_message(f"🏷️ Cleared {member.mention}'s title in **{crew_name}**.")


def setup(bot):
    bot.tree.add_command(crew_group)