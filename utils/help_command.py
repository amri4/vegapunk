import discord
from discord.ext import commands


# =========================================================
# DATABASE
# =========================================================

import mycord

db = mycord.DB()


# =========================================================
# CATEGORY
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
# SLASH COMMANDS
# =========================================================

def get_slash_commands(bot):

    commands_list = []

    for command in bot.tree.get_commands():

        if command.name == "help":
            continue

        commands_list.append(command)

    return commands_list


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

        self.category = list(
            categories.keys()
        )[0]

        self.page = 0
        self.per_page = 6

        self.add_item(
            CategorySelect(self)
        )

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
    # SLASH MENTION
    # -----------------------------------------------------

    def get_slash_name(self, command):

        command_id = getattr(
            command,
            "id",
            None
        )

        if command_id:

            return (
                f"</{command.qualified_name}:"
                f"{command_id}>"
            )

        return f"/{command.qualified_name}"

    # -----------------------------------------------------
    # COMMAND DISPLAY
    # -----------------------------------------------------

    def get_command_name(self, command):

        # Slash-only command
        if isinstance(
            command,
            discord.app_commands.Command
        ):

            return self.get_slash_name(
                command
            )

        # Prefix / hybrid command
        prefix = self.prefix

        name = f"`{prefix}{command.qualified_name}`"

        app_command = getattr(
            command,
            "app_command",
            None
        )

        if app_command:

            slash = self.get_slash_name(
                app_command
            )

            return f"{name} • {slash}"

        return name

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
            "Choose a category from the menu below."
        )

        if not pages:

            embed.add_field(
                name="No Commands",
                value=(
                    "There are no commands "
                    "in this category."
                ),
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
    # BUTTON STATE
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

class CategorySelect(
    discord.ui.Select
):

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

        self.help_view.category_select = CategorySelect(
            self.help_view
        )

        await interaction.response.edit_message(
            embed=self.help_view.get_embed(),
            view=self.help_view
        )


# =========================================================
# HELP COMMAND
# =========================================================

class BotHelpCommand(
    commands.HelpCommand
):

    # -----------------------------------------------------
    # CATEGORY
    # -----------------------------------------------------

    def get_command_category(self, command):

        return get_category(command)

    # -----------------------------------------------------
    # COLLECT COMMANDS
    # -----------------------------------------------------

    def collect_commands(self):

        categories = {}

        # =================================================
        # PREFIX / HYBRID COMMANDS
        # =================================================

        for command in self.bot.commands:

            if command.hidden:
                continue

            category = self.get_command_category(
                command
            )

            categories.setdefault(
                category,
                []
            )

            categories[category].append(
                command
            )

        # =================================================
        # SLASH-ONLY COMMANDS
        # =================================================

        slash_commands = get_slash_commands(
            self.bot
        )

        for command in slash_commands:

            # Don't duplicate hybrid commands
            duplicate = False

            for prefix_command in self.bot.commands:

                app_command = getattr(
                    prefix_command,
                    "app_command",
                    None
                )

                if not app_command:
                    continue

                if app_command.name == command.name:

                    duplicate = True
                    break

            if duplicate:
                continue

            category = get_category(
                command
            )

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
            or command.description
            or "No description."
        )

        embed.description = description

        prefix = self.get_prefix()

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

            command_id = getattr(
                app_command,
                "id",
                None
            )

            if command_id:

                slash = (
                    f"</{app_command.qualified_name}:"
                    f"{command_id}>"
                )

            else:

                slash = (
                    f"/"
                    f"{app_command.qualified_name}"
                )

            embed.add_field(
                name="Slash",
                value=slash,
                inline=False
            )

        await self.get_destination().send(
            embed=embed
        )


# =========================================================
# EXPORT
# =========================================================

help_command = BotHelpCommand()