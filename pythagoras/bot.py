import os
import discord
from discord.ext import commands
from pathlib import Path


class Bot(commands.Bot):

    def __init__(self):
        self.bot_name = Path(__file__).parent.name

        super().__init__(
            command_prefix="Pythagoras ",
            intents=discord.Intents.all(),
            help_command=None,
            application_id=int(os.getenv("PYTHAGORAS_APPLICATION_ID"))
        )

    async def setup_hook(self):
        await self.tree.sync()
        print(f"[{self.bot_name}] Slash commands synced.")
    
    async def on_ready(self):
        print(f"[{self.bot_name}] Logged in as {self.user}")


bot = Bot()