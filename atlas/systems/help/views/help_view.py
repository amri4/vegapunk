import discord

from ..functions.commands import get_slash_commands
from ..functions.embed import build_help_embed
from ..buttons.navigation import PreviousButton, NextButton


class HelpView(discord.ui.View):

    def __init__(self, bot, author):
        super().__init__(timeout=180)

        self.bot = bot
        self.author = author
        self.page = 0

        self.categories = get_slash_commands(self.bot)
        self.category_names = list(self.categories.keys())

        self.add_item(PreviousButton(self))
        self.add_item(NextButton(self))

    def update_buttons(self):
        for item in self.children:
            if hasattr(item, "update_state"):
                item.update_state()

    def refresh(self):
        self.categories = get_slash_commands(self.bot)
        self.category_names = list(self.categories.keys())

        if self.page >= len(self.category_names):
            self.page = max(0, len(self.category_names) - 1)

    
    async def embed(self):
        return await build_help_embed(
            self.bot,
            self.categories,
            self.category_names,
            self.page
        )

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True