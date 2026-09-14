import mycord

db = mycord.DB()


async def on_member_join(member):
    welcome = db.fetchone(
        "welcome",
        "guild_id = ?",
        (member.guild.id,)
    )

    if welcome is None:
        return

    channel_id = welcome[1]

    channel = member.guild.get_channel(channel_id)

    if channel is None:
        return

    await channel.send(
        f"👋 Welcome {member.mention} to **{member.guild.name}**!"
    )


def setup(bot):
    bot.add_listener(on_member_join)