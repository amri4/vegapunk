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
    post_id INTEGER,
    PRIMARY KEY(user_id, guild_id)
    """
)
db.create_table(
    "game_channels",
    """
    guild_id INTEGER PRIMARY KEY,
    forum_id INTEGER
    """
)

#-----------FUNCTIONS------------
# SETUP ISLAND FORUM
async def setup_island_forum(interaction: discord.Interaction, guild: discord.Guild, text: str):

    # Get saved data
    data_channels = db.fetchone(
        "game_channels",
        "guild_id = ?",
        (guild.id,)
    )
    data_profile = db.fetchone(
        "profiles",
        "user_id = ? AND guild_id = ?",
        (interaction.user.id, guild.id)
    )

    # Unpack database result
    forum_id = data_channels[1] if data_channels else None
    post_id = data_profile[3] if data_profile else None

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
            name=text,
            content="Welcome to Island Conquest! 🏝️"
        )

        post_id = post.id

    # Save IDs
    db.insert_replace(
        "game_channels",
        "guild_id, forum_id",
        (guild.id, forum_id)
    )
    db.update(
        "profiles",
        "post_id = ?",
        (post.id,),
        "user_id = ? AND guild_id = ?",
        (interaction.user.id, guild.id)
    )

    return forum, post

#-----------COMMANDS------------
conquest_commands = app_commands.Group(
    name="conquest",
    description="island conquest commands"
)

@conquest_commands.command(
    name="create_profile",
    description="create your island conquest profile"
)
async def create_profile(
    interaction: discord.Interaction,
    island_name: str
):
    await interaction.response.defer(ephemeral=True)
    
    player_exists = db.exists(
        "profiles",
        "user_id = ? AND guild_id = ?",
        (interaction.user.id, interaction.guild.id)
    )

    island_exists = db.exists(
        "profiles",
        "island_name = ? COLLATE NOCASE AND guild_id = ?",
        (island_name, interaction.guild.id)
    )
    if player_exists:
        await interaction.followup.send(
            "You already have a profile",
            ephemeral=True
        )
        return
    if island_exists:
        await interaction.followup.send(
            "This island already exists, try another name",
            ephemeral=True
        )
        return
    db.insert(
        "profiles",
        "user_id, guild_id, island_name",
        (interaction.user.id, interaction.guild.id, island_name)
    )
    forum, post = await setup_island_forum(interaction, interaction.guild, island_name)

    await interaction.followup.send(
        "Your island has been created!\n"
        f"{post.mention}"
    )

def setup(bot):
    bot.tree.add_command(conquest_commands)