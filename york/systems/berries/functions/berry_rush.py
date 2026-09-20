import asyncio
import random
import discord


rush_active = False


async def start_berry_rush(bot, channel_id):
    global rush_active

    if rush_active:
        return

    rush_active = True

    channel = bot.get_channel(channel_id)

    if channel:
        embed = discord.Embed(
            title="💰 BERRY RUSH!",
            description=(
                "The seas are overflowing with berries!\n\n"
                f"<:berries:1550458400800776344> **All message earnings are now ×2!**\n"
                "⏰ The rush lasts for **30 minutes**."
            ),
            color=discord.Color.gold()
        )

        await channel.send(embed=embed)

    await asyncio.sleep(30 * 60)

    rush_active = False

    if channel:
        embed = discord.Embed(
            title="🏴‍☠️ Berry Rush Over!",
            description="The Berry Rush has ended. Back to normal berry earnings!",
            color=discord.Color.blue()
        )

        await channel.send(embed=embed)


def berry_multiplier():
    return 2 if rush_active else 1


async def berry_rush_loop(bot, channel_id):
    while not bot.is_closed():
        # Wait 6 hours before another possible rush
        await asyncio.sleep(6 * 60 * 60)

        # 50% chance to actually start one
        if random.random() < 0.5:
            await start_berry_rush(bot, channel_id)