import discord

from ..functions.arrange_roles import arrange_roles


async def on_guild_role_update(
    before: discord.Role,
    after: discord.Role
):

    guild = after.guild

    bot_member = guild.me

    if bot_member is None:
        return

    # Only react when Lilith's highest role
    # itself has been moved.
    if after.id != bot_member.top_role.id:
        return

    if before.position == after.position:
        return

    await arrange_roles(guild)


def setup(bot):
    bot.add_listener(
        on_guild_role_update,
        "on_guild_role_update"
    )