import discord
from discord.ext import commands
from pathlib import Path
from utils.help_command import help_command


class Bot(commands.Bot):

    def __init__(self):
        self.bot_name = Path(__file__).parent.name

        super().__init__(
            command_prefix="Atlas ",
            intents=discord.Intents.all(),
            help_command=help_command
        )

    async def on_ready(self):
        print(f"[{self.bot_name}] Logged in as {self.user}")


bot = Bot()