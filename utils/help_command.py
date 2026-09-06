import discord
from discord import app_commands


# =========================================================
# COMMAND CATEGORIES
# =========================================================

def get_category(command):

    module = getattr(command, "module", "")

    parts = module.split(".")

    if "systems" in parts:

        index = parts.index("systems")

        if index + 1 < len(parts):
            return parts[index + 1].replace(
                "_", " "
            ).title()

    return "General"


# =========================================================
# GET COMMANDS
# =========================================================

def get_commands(bot):

    commands = []

    for command in bot.tree.get_commands():

        if command.name == "help":
            continue

        commands.append(command)

    return commands


# =========================================================
# HELP VIEW
# =========================================================

class HelpView(discord.ui.View):

    def __init__(
        self,
        bot,
        user_id,
        categories
    ):
        super().__init__(timeout=180)

        self.bot = bot
        self.user_id = user_id
        self.categories = categories

        self.category = list(categories.keys())[0]
        self.page = 0

        self.per_page = 6

        self.category_select = CategorySelect(
            self
        )

        self.add_item(self.category_select)

        self.update_buttons()

    # -----------------------------------------------------
    # CURRENT COMMANDS
    # -----------------------------------------------------

    def current_commands(self):

        return self.categories.get(
            self.category,
            []
        )

    # -----------------------------------------------------
    # PAGES
    # -----------------------------------------------------

    def get_pages(self):

        commands = self.current_commands()

        return [
            commands[i:i + self.per_page]
            for i in range(
                0,
                len(commands),
                self.per_page
            )
        ]

    # -----------------------------------------------------
    # EMBED
    # -----------------------------------------------------

    def get_embed(self):

        pages = self.get_pages()

        embed = discord.Embed(
            title=f"{self.bot.bot_name} Help",
            color=discord.Color.blurple()
        )

        embed.description = (
            f"**Category:** {self.category}\n"
            "Select a category below."
        )

        if not pages:

            embed.add_field(
                name="No Commands",
                value="There are no commands in this category.",
                inline=False
            )

            return embed

        for command in pages[self.page]:

            embed.add_field(
                name=f"/{command.qualified_name}",
                value=command.description or "No description.",
                inline=False
            )

        embed.set_footer(
            text=(
                f"Page {self.page + 1}/{len(pages)}"
            )
        )

        return embed

    # -----------------------------------------------------
    # BUTTONS
    # -----------------------------------------------------

    def update_buttons(self):

        pages = self.get_pages()

        self.previous.disabled = (
            self.page <= 0
        )

        self.next.disabled = (
            not pages or
            self.page >= len(pages) - 1
        )

    # -----------------------------------------------------
    # PREVIOUS
    # -----------------------------------------------------

    @discord.ui.button(
        label="Previous",
        style=discord.ButtonStyle.secondary
    )
    async def previous(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        self.page -= 1

        self.update_buttons()

        await interaction.response.edit_message(
            embed=self.get_embed(),
            view=self
        )

    # -----------------------------------------------------
    # NEXT
    # -----------------------------------------------------

    @discord.ui.button(
        label="Next",
        style=discord.ButtonStyle.primary
    )
    async def next(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        self.page += 1

        self.update_buttons()

        await interaction.response.edit_message(
            embed=self.get_embed(),
            view=self
        )

    # -----------------------------------------------------
    # INTERACTION CHECK
    # -----------------------------------------------------

    async def interaction_check(
        self,
        interaction: discord.Interaction
    ):

        if interaction.user.id != self.user_id:

            await interaction.response.send_message(
                "This help menu isn't yours.",
                ephemeral=True
            )

            return False

        return True


# =========================================================
# CATEGORY SELECT
# =========================================================

class CategorySelect(
    discord.ui.Select
):

    def __init__(self, view):

        self.help_view = view

        options = []

        for category in view.categories:

            options.append(
                discord.SelectOption(
                    label=category,
                    value=category
                )
            )

        super().__init__(
            placeholder="Choose a category...",
            options=options
        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        self.help_view.category = self.values[0]
        self.help_view.page = 0

        self.help_view.update_buttons()

        await interaction.response.edit_message(
            embed=self.help_view.get_embed(),
            view=self.help_view
        )


# =========================================================
# HELP COMMAND
# =========================================================

@app_commands.command(
    name="help",
    description="Show all available commands"
)
async def help_command(
    interaction: discord.Interaction
):

    bot = interaction.client

    all_commands = get_commands(bot)

    categories = {}

    for command in all_commands:

        category = get_category(command)

        categories.setdefault(
            category,
            []
        )

        categories[category].append(
            command
        )

    for category in categories:

        categories[category].sort(
            key=lambda command:
            command.qualified_name
        )

    if not categories:

        await interaction.response.send_message(
            "There are no commands available.",
            ephemeral=True
        )

        return

    view = HelpView(
        bot,
        interaction.user.id,
        categories
    )

    await interaction.response.send_message(
        embed=view.get_embed(),
        view=view
    )


# =========================================================
# SETUP
# =========================================================

def setup(bot):

    bot.tree.add_command(
        help_command
    )