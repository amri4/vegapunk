import random
import time

from ..functions.berries import add_berries


COOLDOWN = 5

cooldowns = {}


async def on_message(message):
    if message.author.bot:
        return

    if message.guild is None:
        return

    key = (
        message.guild.id,
        message.author.id
    )

    current_time = time.monotonic()

    last_message = cooldowns.get(
        key,
        0
    )

    if current_time - last_message < COOLDOWN:
        return

    cooldowns[key] = current_time

    amount = random.randint(
        1,
        5
    )

    add_berries(
        message.guild.id,
        message.author.id,
        amount
    )


def setup(bot):
    bot.add_listener(
        on_message
    )