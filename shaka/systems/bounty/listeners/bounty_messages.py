import discord
import random

from ..functions.add_bounty import add_bounty


async def on_message(message: discord.Message):

    if message.author.bot:
        return

    if message.guild is None:
        return

    added_bounty = random.randint(5, 20)

    add_bounty(
        message.guild.id,
        message.author.id,
        added_bounty
    )