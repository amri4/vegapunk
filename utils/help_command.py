import discord
from discord.ext import commands


class HelpView(discord.ui.View):

    def __init__(self, pages, author):
        super().__init__(timeout=120)

        self.pages = pages
        self.author = author
        self.page = 0

        self.update_buttons()

    def update_buttons(self):
        self.previous.disabled = self.page == 0
        self.next.disabled = self.page == len(self.pages) - 1

        self.page_button.label = f"{self.page + 1} / {len(self.pages)}"

    def get_embed(self):
        category, commands_list = self.pages[self.page]

        embed = discord.Embed(
            title="📖 Help",
            description=f"**{category.title()}**"
        )

        for command in commands_list:
            description = command.help or "No description."

            embed.add_field(
                name=f"`{command.name}`",
                value=description,
                inline=False
            )

        return embed

    async def interaction_check(self, interaction):
        if interaction.user != self.author:
            await interaction.response.send_message(
                "This help menu isn't yours.",
                ephemeral=True
            )
            return False

        return True

    @discord.ui.button(
        label="◀️",
        style=discord.ButtonStyle.secondary
    )
    async def previous(self, interaction, button):

        if self.page > 0:
            self.page -= 1

        self.update_buttons()

        await interaction.response.edit_message(
            embed=self.get_embed(),
            view=self
        )

    @discord.ui.button(
        label="1 / 1",
        style=discord.ButtonStyle.secondary,
        disabled=True
    )
    async def page_button(self, interaction, button):
        pass

    @discord.ui.button(
        label="▶️",
        style=discord.ButtonStyle.secondary
    )
    async def next(self, interaction, button):

        if self.page < len(self.pages) - 1:
            self.page += 1

        self.update_buttons()

        await interaction.response.edit_message(
            embed=self.get_embed(),
            view=self
        )


class BotHelpCommand(commands.HelpCommand):

    async def send_bot_help(self, mapping):

        bot = self.context.bot

        categories = {}

        for command in bot.commands:

            # Ignore hidden commands
            if command.hidden:
                continue

            module = command.callback.__module__

            parts = module.split(".")

            # Expected:
            # bot.systems.category.commands.file
            try:
                systems_index = parts.index("systems")
                category = parts[systems_index + 1]

            except (ValueError, IndexError):
                category = "Other"

            categories.setdefault(category, [])

            categories[category].append(command)

        pages = []

        for category, commands_list in categories.items():

            commands_list.sort(key=lambda command: command.name)

            pages.append(
                (category, commands_list)
            )

        if not pages:
            await self.get_destination().send(
                "There are no commands available."
            )
            return

        view = HelpView(
            pages,
            self.context.author
        )

        await self.get_destination().send(
            embed=view.get_embed(),
            view=view
        )


help_command = BotHelpCommand()