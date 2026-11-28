import discord
from discord import app_commands
import mycord

db = mycord.DB()

db.create_table(
    "profiles",
    """
    user_id INTEGER,
    guild_id INTEGER,
    island_name TEXT,
    PRIMARY KEY(user_id, guild_id)
    """
)
db.create_table(
    "game_channels",
    """
    guild_id INTEGER PRIMARY KEY,
    forum_id INTEGER,
    post_id INTEGER
    """
)

#-----------FUNCTIONS------------
# SETUP ISLAND FORUM
async def setup_island_forum(guild: discord.Guild, text):

    # Get saved data
    data = db.fetchone(
        "game_channels",
        "guild_id = ?",
        (guild.id,)
    )

    # Unpack database result
    if data:
        _, forum_id, post_id = data
    else:
        forum_id = None
        post_id = None

    # Check forum
    forum = guild.get_channel(forum_id) if forum_id else None

    if not isinstance(forum, discord.ForumChannel):

        forum = await guild.create_forum(
            name="island-conquest"
        )

        forum_id = forum.id
        post_id = None

    # Check post
    post = None

    if post_id:
        try:
            post = await guild.fetch_channel(post_id)
        except discord.NotFound:
            post = None

    if not isinstance(post, discord.Thread):

        post, message = await forum.create_thread(
            name=f"{text}",
            content="Welcome to Island Conquest! 🏝️"
        )

        post_id = post.id

    # Save IDs
    db.insert_replace(
        "game_channels",
        "guild_id, forum_id, post_id",
        (guild.id, forum_id, post_id)
    )

    return forum, post

#-----------COMMANDS------------
conquest_commands = app_commands.Group(
    name="conquest",
    description="island conquest commands"
)

conquest_commands.command(
    name="create_profile",
    description="create your island conquest profile"
)
async def create_profile(
    interaction: discord.Interaction,
    island_name: str
):
    player_exists = db.fetchone(
        "profiles",
        "user_id = ? AND guild_id = ?",
        (interaction.user.id, interaction.guild.id)
    )
    if player_exists:
        await interaction.response.send_message(
            "You already have a profile",
            ephemeral=True
        )
        return
    db.insert(
        "profiles",
        "user_id, guild_id, island_name",
        (interaction.user.id, interaction.guild.id, island_name)
    )
    forum, post = await setup_island_forum(interaction.guild, island_name)

    await interaction.response.send_message(
        "Profile created. Here is your island:\n"
        f"{post.mention}"
    )

def setup(bot):
    bot.tree.add_command(conquest_commands)