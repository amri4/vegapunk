import os
import discord
from discord.ext import commands
from pathlib import Path


class Bot(commands.Bot):

    def __init__(self):
        self.bot_name = Path(__file__).parent.name

        super().__init__(
            command_prefix="Atlas ",
            intents=discord.Intents.all(),
            application_id=int(os.getenv("ATLAS_APPLICATION_ID"))
        )

    async def on_ready():
        print(f"[{self.bot_name}] Logged in as {self.user}")


bot = Bot()