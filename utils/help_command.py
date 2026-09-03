import discord
from discord.ext import commands

import mycord


db = mycord.PunksDB()


# =========================================
# STAFF RANK
# =========================================

def get_command_rank(guild, command_name):

    if guild is None:
        return None

    command_rank = db.fetchone(
        "command_ranks",
        "guild_id = ? AND command_name = ?",
        (
            guild.id,
            command_name.lower()
        )
    )

    if command_rank is None:
        return None

    rank = db.fetchone(
        "staff_ranks",
        "guild_id = ? AND level = ?",
        (
            guild.id,
            command_rank["required_level"]
        )
    )

    return rank


# =========================================
# HELP VIEW
# =========================================

class HelpView(discord.ui.View):

    def __init__(self, pages, author, guild):
        super().__init__(timeout=120)

        self.pages = pages
        self.author = author
        self.guild = guild
        self.page = 0

        self.update_buttons()

    # =====================================
    # BUTTON STATE
    # =====================================

    def update_buttons(self):

        self.previous.disabled = self.page == 0

        self.next.disabled = (
            self.page == len(self.pages) - 1
        )

        self.page_button.label = (
            f"{self.page + 1} / {len(self.pages)}"
        )

    # =====================================
    # EMBED
    # =====================================

    def get_embed(self):

        category, commands_list = self.pages[self.page]

        embed = discord.Embed(
            title="📖 Help",
            description=f"**{category.title()}**"
        )

        for command in commands_list:

            description = command.help or "No description."

            rank = get_command_rank(
                self.guild,
                command.name
            )

            if rank:

                description += (
                    f"\n\n**Required rank:** "
                    f"{rank['name']} or above"
                )

            embed.add_field(
                name=f"`{command.name}`",
                value=description,
                inline=False
            )

        return embed

    # =====================================
    # ONLY COMMAND USER CAN USE BUTTONS
    # =====================================

    async def interaction_check(self, interaction):

        if interaction.user != self.author:

            await interaction.response.send_message(
                "This help menu isn't yours.",
                ephemeral=True
            )

            return False

        return True

    # =====================================
    # PREVIOUS
    # =====================================

    @discord.ui.button(
        label="◀️",
        style=discord.ButtonStyle.secondary
    )
    async def previous(self, interaction, button):

        await interaction.response.defer()

        if self.page > 0:
            self.page -= 1

        self.update_buttons()

        await interaction.edit_original_response(
            embed=self.get_embed(),
            view=self
        )

    # =====================================
    # PAGE NUMBER
    # =====================================

    @discord.ui.button(
        label="1 / 1",
        style=discord.ButtonStyle.secondary,
        disabled=True
    )
    async def page_button(self, interaction, button):

        pass

    # =====================================
    # NEXT
    # =====================================

    @discord.ui.button(
        label="▶️",
        style=discord.ButtonStyle.secondary
    )
    async def next(self, interaction, button):

        await interaction.response.defer()

        if self.page < len(self.pages) - 1:
            self.page += 1

        self.update_buttons()

        await interaction.edit_original_response(
            embed=self.get_embed(),
            view=self
        )


# =========================================
# HELP COMMAND
# =========================================

class BotHelpCommand(commands.HelpCommand):

    # =====================================
    # CATEGORY
    # =====================================

    def get_category(self, command):

        module = command.callback.__module__

        parts = module.split(".")

        try:

            systems_index = parts.index("systems")

            return parts[systems_index + 1]

        except (ValueError, IndexError):

            return "Other"

    # =====================================
    # SEND ALL HELP
    # =====================================

    async def send_bot_help(self, mapping):

        bot = self.context.bot

        categories = {}

        for command in bot.commands:

            if command.hidden:
                continue

            category = self.get_category(command)

            categories.setdefault(category, [])

            categories[category].append(command)

        pages = []

        for category, commands_list in categories.items():

            commands_list.sort(
                key=lambda command: command.name
            )

            pages.append(
                (category, commands_list)
            )

        # =================================
        # SORT CATEGORIES
        # =================================

        pages.sort(
            key=lambda page: page[0].lower()
        )

        if not pages:

            await self.get_destination().send(
                "There are no commands available."
            )

            return

        view = HelpView(
            pages,
            self.context.author,
            self.context.guild
        )

        await self.get_destination().send(
            embed=view.get_embed(),
            view=view
        )

    # =====================================
    # SEND COMMAND HELP
    # =====================================

    async def send_command_help(self, command):

        if command.hidden:

            await self.get_destination().send(
                "That command doesn't exist."
            )

            return

        category = self.get_category(command)

        prefix = self.context.bot.command_prefix

        # =================================
        # GET PREFIX
        # =================================

        if callable(prefix):

            prefix = await prefix(
                self.context.bot,
                self.context.message
            )

        # =================================
        # AUTOMATIC USAGE
        # =================================

        if command.usage:

            usage = command.usage

        else:

            usage_parts = []

            for parameter in command.clean_params.values():

                name = parameter.name

                # *args / **kwargs style parameter

                if parameter.kind == parameter.VAR_POSITIONAL:

                    usage_parts.append(
                        f"[{name}...]"
                    )

                # Parameter has a default value

                elif parameter.default is not parameter.empty:

                    usage_parts.append(
                        f"[{name}]"
                    )

                # Required parameter

                else:

                    usage_parts.append(
                        f"<{name}>"
                    )

            usage = " ".join(usage_parts)

        # =================================
        # FULL USAGE
        # =================================

        full_usage = f"{prefix}{command.name}"

        if usage:

            full_usage += f" {usage}"

        # =================================
        # EMBED
        # =================================

        embed = discord.Embed(
            title=f"📖 {command.name}",
            description=command.help or "No description."
        )

        embed.add_field(
            name="Usage",
            value=f"`{full_usage}`",
            inline=False
        )

        embed.add_field(
            name="Category",
            value=category.title(),
            inline=False
        )

        # =================================
        # REQUIRED RANK
        # =================================

        rank = get_command_rank(
            self.context.guild,
            command.name
        )

        if rank:

            embed.add_field(
                name="Required rank",
                value=f"{rank['name']} or above",
                inline=False
            )

        # =================================
        # ALIASES
        # =================================

        if command.aliases:

            aliases = ", ".join(
                f"`{alias}`"
                for alias in command.aliases
            )

            embed.add_field(
                name="Aliases",
                value=aliases,
                inline=False
            )

        await self.get_destination().send(
            embed=embed
        )


# =========================================
# HELP COMMAND INSTANCE
# =========================================

help_command = BotHelpCommand()