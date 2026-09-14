import mycord
import discord

db = mycord.DB()


async def on_member_join(member):
    welcome = db.fetchone(
        "welcome",
        "guild_id = ?",
        (member.guild.id,)
    )

    if welcome is None:
        return

    embed = discord.Embed(
        title=f"Welcome to {member.guild.name}",
        description="**The seas have gained another pirate!**\n Welcome aboard! Your adventure starts here."
    )
    embed.set_footer(text=f"You're the {member.guild.member_count}th member in this server'")

    channel_id = welcome[1]

    channel = member.guild.get_channel(channel_id)

    if channel is None:
        return

    await channel.send(
        embed=embed
    )


def setup(bot):
    bot.add_listener(on_member_join)