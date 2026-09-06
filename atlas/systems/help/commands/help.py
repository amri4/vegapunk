import discord
from discord.ext import commands
from discord import app_commands

from pathlib import Path


# =========================================================
# HELP DATA
# =========================================================

def get_category(callback):
    """Get category from systems/<category>/commands/<file>.py"""

    try:
        file = Path(callback.__code__.co_filename)
        parts = file.parts

        if "systems" in parts:
            index = parts.index("systems")

            if index + 1 < len(parts):
                return parts[index + 1].replace("_", " ").title()

    except Exception:
        pass

    return "Other"


def get_prefix_commands(bot):
    categories = {}

    for command in bot.commands:
        # Don't show this help command inside itself
        if command.name == "help":
            continue

        category = get_category(command.callback)

        categories.setdefault(category, [])
        categories[category].append(command)

    return dict(sorted(categories.items()))


def get_slash_commands(bot):
    categories = {}

    for command in bot.tree.get_commands():

        # Ignore slash groups for now
        if isinstance(command, app_commands.Group):
            continue

        # Don't show this help command inside itself
        if command.name == "help":
            continue

        category = get_category(command.callback)

        categories.setdefault(category, [])
        categories[category].append(command)

    return dict(sorted(categories.items()))


# =========================================================
# HELP VIEW
# =========================================================

class HelpView(discord.ui.View):

    def __init__(self, bot, author):
        super().__init__(timeout=180)

        self.bot = bot
        self.author = author

        self.mode = "prefix"
        self.page = 0

        self.categories = {}
        self.category_names = []

        self.refresh_data()

    # -----------------------------------------------------
    # Refresh commands
    # -----------------------------------------------------

    def refresh_data(self):

        if self.mode == "prefix":
            self.categories = get_prefix_commands(self.bot)
        else:
            self.categories = get_slash_commands(self.bot)

        self.category_names = list(self.categories.keys())

        if self.page >= len(self.category_names):
            self.page = max(0, len(self.category_names) - 1)

    # -----------------------------------------------------
    # Get prefix
    # -----------------------------------------------------

    def get_prefix(self):

        prefix = self.bot.command_prefix

        if callable(prefix):
            return ""

        if isinstance(prefix, (list, tuple)):
            return prefix[0] if prefix else ""

        return prefix

    # -----------------------------------------------------
    # Make embed
    # -----------------------------------------------------

    def make_embed(self):

        embed = discord.Embed(
            title="📖 Atlas Help"
        )

        if self.mode == "prefix":
            embed.description = "💬 **Prefix Commands**"
        else:
            embed.description = "⚡ **Slash Commands**"

        if not self.category_names:
            embed.add_field(
                name="No commands",
                value="No commands were found.",
                inline=False
            )

            return embed

        category = self.category_names[self.page]
        command_list = self.categories[category]

        lines = []

        for command in command_list:

            # =============================================
            # PREFIX
            # =============================================

            if self.mode == "prefix":

                prefix = self.get_prefix()

                usage = command.usage

                if usage:
                    usage_text = f"{prefix}{usage}"
                else:
                    usage_text = f"{prefix}{command.name}"

                description = command.description

                if not description:
                    description = "No description provided."

                lines.append(
                    f"**`{usage_text}`**\n"
                    f"{description}"
                )

            # =============================================
            # SLASH
            # =============================================

            else:

                if command.id:
                    command_name = (
                        f"</{command.qualified_name}:{command.id}>"
                    )
                else:
                    command_name = (
                        f"`/{command.qualified_name}`"
                    )

                description = command.description

                if not description:
                    description = "No description provided."

                lines.append(
                    f"**{command_name}**\n"
                    f"{description}"
                )

        embed.add_field(
            name=f"📂 {category}",
            value="\n\n".join(lines),
            inline=False
        )

        embed.set_footer(
            text=(
                f"Category {self.page + 1}"
                f"/{len(self.category_names)}"
            )
        )

        return embed

    # =====================================================
    # SELECT MENU
    # =====================================================

    @discord.ui.select(
        placeholder="Choose command type...",
        options=[
            discord.SelectOption(
                label="Prefix Commands",
                value="prefix",
                description="Show prefix commands",
                emoji="💬"
            ),
            discord.SelectOption(
                label="Slash Commands",
                value="slash",
                description="Show slash commands",
                emoji="⚡"
            )
        ]
    )
    async def command_type(
        self,
        interaction: discord.Interaction,
        select: discord.ui.Select
    ):

        if interaction.user.id != self.author.id:
            await interaction.response.send_message(
                "This help menu belongs to someone else.",
                ephemeral=True
            )
            return

        self.mode = select.values[0]
        self.page = 0

        self.refresh_data()

        await interaction.response.edit_message(
            embed=self.make_embed(),
            view=self
        )

    # =====================================================
    # PREVIOUS
    # =====================================================

    @discord.ui.button(
        emoji="◀️",
        style=discord.ButtonStyle.secondary
    )
    async def previous(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if interaction.user.id != self.author.id:
            await interaction.response.send_message(
                "This help menu belongs to someone else.",
                ephemeral=True
            )
            return

        if not self.category_names:
            await interaction.response.defer()
            return

        self.page -= 1

        if self.page < 0:
            self.page = len(self.category_names) - 1

        await interaction.response.edit_message(
            embed=self.make_embed(),
            view=self
        )

    # =====================================================
    # NEXT
    # =====================================================

    @discord.ui.button(
        emoji="▶️",
        style=discord.ButtonStyle.secondary
    )
    async def next(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if interaction.user.id != self.author.id:
            await interaction.response.send_message(
                "This help menu belongs to someone else.",
                ephemeral=True
            )
            return

        if not self.category_names:
            await interaction.response.defer()
            return

        self.page += 1

        if self.page >= len(self.category_names):
            self.page = 0

        await interaction.response.edit_message(
            embed=self.make_embed(),
            view=self
        )

    # =====================================================
    # TIMEOUT
    # =====================================================

    async def on_timeout(self):

        for item in self.children:
            item.disabled = True


# =========================================================
# PREFIX COMMAND
# =========================================================

@commands.command(
    name="help",
    description="Show Atlas commands."
)
async def help_command(ctx):

    view = HelpView(
        ctx.bot,
        ctx.author
    )

    await ctx.send(
        embed=view.make_embed(),
        view=view
    )


# =========================================================
# SLASH COMMAND
# =========================================================

@app_commands.command(
    name="help",
    description="Show Atlas commands."
)
async def slash_help(interaction: discord.Interaction):

    view = HelpView(
        interaction.client,
        interaction.user
    )

    await interaction.response.send_message(
        embed=view.make_embed(),
        view=view
    )


# =========================================================
# SETUP
# =========================================================

async def setup(bot):

    bot.add_command(help_command)
    bot.tree.add_command(slash_help)