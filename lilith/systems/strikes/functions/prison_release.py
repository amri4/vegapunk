import asyncio
import time

from ..ids import PRISON_ROLE_ID
from ..functions.prison import release
import mycord

db = mycord.DB()


async def prison_release_loop(bot):
    await bot.wait_until_ready()

    while not bot.is_closed():
        rows = db.fetchall("strikes")

        for row in rows:
            guild_id = row[0]
            user_id = row[1]
            prison_until = row[3]

            if prison_until is None:
                continue

            if int(time.time()) < prison_until:
                continue

            guild = bot.get_guild(guild_id)

            if guild is not None:
                member = guild.get_member(user_id)

                if member is not None:
                    role = guild.get_role(PRISON_ROLE_ID)

                    if role is not None and role in member.roles:
                        await member.remove_roles(role)

            release(guild_id, user_id)

        await asyncio.sleep(60)


def setup(bot):
    bot.loop.create_task(prison_release_loop(bot))