import discord

from ..functions.commands import (
    get_prefix_commands,
    get_slash_commands
)

from ..functions.embed import build_help_embed

from ..selects.command_type import CommandTypeSelect
from ..buttons.navigation import PreviousButton, NextButton


class HelpView(discord.ui.View):

    def __init__(self, bot, author):

        super().__init__(timeout=180)

        self.bot = bot
        self.author = author

        self.mode = "prefix"
        self.page = 0

        self.categories = {}
        self.category_names = []

        self.add_item(CommandTypeSelect(self))
        self.add_item(PreviousButton(self))
        self.add_item(NextButton(self))

        self.refresh()

    def refresh(self):

        if self.mode == "prefix":
            self.categories = get_prefix_commands(self.bot)
        else:
            self.categories = get_slash_commands(self.bot)

        self.category_names = list(
            self.categories.keys()
        )

        if self.page >= len(self.category_names):
            self.page = max(
                0,
                len(self.category_names) - 1
            )

    def embed(self):

        return build_help_embed(
            self.bot,
            self.mode,
            self.categories,
            self.category_names,
            self.page
        )

    async def on_timeout(self):

        for item in self.children:
            item.disabled = True