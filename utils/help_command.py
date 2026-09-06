import discord
from discord.ext import commands


# =========================================================
# CATEGORY
# =========================================================

def get_category(command):

    module = getattr(command, "module", None)

    if module:

        parts = module.split(".")

        if "systems" in parts:

            index = parts.index("systems")

            if index + 1 < len(parts):
                return parts[index + 1].replace(
                    "_", " "
                ).title()

    return "General"


# =========================================================
# SLASH COMMAND NAME
# =========================================================

def get_slash_name(command):

    command_id = getattr(command, "id", None)

    if command_id:
        return f"</{command.qualified_name}:{command_id}>"

    return f"/{command.qualified_name}"


# =========================================================
# HELP VIEW
# =========================================================

class HelpView(discord.ui.View):

    def __init__(
        self,
        bot,
        user_id,
        categories,
        prefix
    ):
        super().__init__(timeout=180)

        self.bot = bot
        self.user_id = user_id
        self.categories = categories
        self.prefix = prefix

        self.category = list(categories.keys())[0]
        self.page = 0
        self.per_page = 6

        self.select = CategorySelect(self)
        self.add_item(self.select)

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

        commands_list = self.current_commands()

        return [
            commands_list[i:i + self.per_page]
            for i in range(
                0,
                len(commands_list),
                self.per_page
            )
        ]

    # -----------------------------------------------------
    # COMMAND NAME
    # -----------------------------------------------------

    def get_command_name(self, command):

        # Slash-only command
        if isinstance(
            command,
            discord.app_commands.Command
        ):
            return get_slash_name(command)

        # Prefix command
        prefix_name = (
            f"`{self.prefix}"
            f"{command.qualified_name}`"
        )

        # Hybrid command
        app_command = getattr(
            command,
            "app_command",
            None
        )

        if app_command:

            slash_name = get_slash_name(
                app_command
            )

            return (
                f"{prefix_name} • "
                f"{slash_name}"
            )

        return prefix_name

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
                value="No commands in this category.",
                inline=False
            )

            return embed

        for command in pages[self.page]:

            description = getattr(
                command,
                "help",
                None
            )

            if not description:

                description = getattr(
                    command,
                    "description",
                    None
                )

            if not description:
                description = "No description."

            embed.add_field(
                name=self.get_command_name(
                    command
                ),
                value=description,
                inline=False
            )

        embed.set_footer(
            text=(
                f"Page {self.page + 1}/"
                f"{len(pages)}"
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
            not pages
            or self.page >= len(pages) - 1
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

class CategorySelect(discord.ui.Select):

    def __init__(self, help_view):

        self.help_view = help_view

        options = []

        for category in help_view.categories:

            options.append(
                discord.SelectOption(
                    label=category,
                    value=category,
                    default=(
                        category
                        == help_view.category
                    )
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

class BotHelpCommand(commands.HelpCommand):

    # -----------------------------------------------------
    # COLLECT COMMANDS
    # -----------------------------------------------------

    def collect_commands(self):

        categories = {}

        # =================================================
        # PREFIX + HYBRID COMMANDS
        # =================================================

        for command in self.bot.commands:

            if command.hidden:
                continue

            category = get_category(command)

            categories.setdefault(
                category,
                []
            )

            categories[category].append(
                command
            )

        # =================================================
        # SLASH COMMANDS
        # =================================================

        for command in self.bot.tree.get_commands():

            if command.name == "help":
                continue

            # Check whether it's already a hybrid command
            duplicate = False

            for prefix_command in self.bot.commands:

                app_command = getattr(
                    prefix_command,
                    "app_command",
                    None
                )

                if not app_command:
                    continue

                if (
                    app_command.name
                    == command.name
                ):
                    duplicate = True
                    break

            if duplicate:
                continue

            category = get_category(command)

            categories.setdefault(
                category,
                []
            )

            categories[category].append(
                command
            )

        # =================================================
        # SORT
        # =================================================

        for category in categories:

            categories[category].sort(
                key=lambda command:
                command.qualified_name
            )

        return categories

    # -----------------------------------------------------
    # BOT HELP
    # -----------------------------------------------------

    async def send_bot_help(self, mapping):

        categories = self.collect_commands()

        if not categories:

            await self.get_destination().send(
                "There are no commands available."
            )

            return

        prefix = self.get_prefix()

        if isinstance(prefix, (list, tuple)):

            prefix = prefix[0]

        view = HelpView(
            self.bot,
            self.context.author.id,
            categories,
            prefix
        )

        await self.get_destination().send(
            embed=view.get_embed(),
            view=view
        )

    # -----------------------------------------------------
    # COMMAND HELP
    # -----------------------------------------------------

    async def send_command_help(self, command):

        embed = discord.Embed(
            title=command.qualified_name,
            color=discord.Color.blurple()
        )

        description = (
            command.help
            or getattr(
                command,
                "description",
                None
            )
            or "No description."
        )

        embed.description = description

        prefix = self.get_prefix()

        if isinstance(prefix, (list, tuple)):
            prefix = prefix[0]

        embed.add_field(
            name="Prefix",
            value=(
                f"`{prefix}"
                f"{command.qualified_name}`"
            ),
            inline=False
        )

        app_command = getattr(
            command,
            "app_command",
            None
        )

        if app_command:

            embed.add_field(
                name="Slash",
                value=get_slash_name(
                    app_command
                ),
                inline=False
            )

        await self.get_destination().send(
            embed=embed
        )


# =========================================================
# EXPORT
# =========================================================

help_command = BotHelpCommand()