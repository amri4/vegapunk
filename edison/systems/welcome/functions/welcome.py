import mycord
import discord

db = mycord.DB()

def ordinal(number):
    if 10 <= number % 100 <= 20:
        suffix = "th"
    else:
        suffix = {
            1: "st",
            2: "nd",
            3: "rd"
        }.get(number % 10, "th")

    return f"{number:,}{suffix}"


async def on_member_join(member):
    welcome = db.fetchone(
        "welcome",
        "guild_id = ?",
        (member.guild.id,)
    )

    if welcome is None:
        return

    faction_channel = discord.utils.get(
        member.guild.text_channels,
        name="choose-faction"
    )

    if faction_channel is None:
        faction_target = "#choose-faction"
    else:
        faction_target = faction_channel.mention

    embed = discord.Embed(
        title=f"Welcome to {member.guild.name}",
        description=(
            f"{member.mention}\n"
            " **The seas have gained another adventurer!**\n"
            " Welcome aboard! Your adventure starts here.\n"
            f" Check {faction_target} to choose your side."
        )
    )
    member_count = member.guild.member_count
    embed.set_footer(text=f"You're the {ordinal(member_count)} member in this server'")

    channel_id = welcome[1]

    channel = member.guild.get_channel(channel_id)

    if channel is None:
        return

    await channel.send(
        embed=embed
    )

    if faction_channel is not None:
        try:
            await faction_channel.send(
                f"{member.mention} Choose your faction above!",
                delete_after=10
            )
        except discord.Forbidden:
            pass

def setup(bot):
    bot.add_listener(on_member_join)