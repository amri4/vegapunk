import discord
from discord.ext import commands
from pathlib import Path
import os

from dotenv import load_dotenv


load_dotenv()


class Bot(commands.Bot):

    def __init__(self):
        self.bot_name = Path(__file__).parent.name
        self.token = os.getenv("ATLAS_TOKEN")

        super().__init__(
            command_prefix="Atlas ",
            intents=discord.Intents.all()
        )

    async def on_ready(self):
        print(f"[{self.bot_name}] Logged in as {self.user}")


bot = Bot()