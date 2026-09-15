import discord
import mycord

from utils.role_colors import parse_role_color


db = mycord.DB()


# =========================================
# ASK MESSAGE
# =========================================

async def ask_message(interaction, question, timeout=300):

    await interaction.followup.send(
        question
    )

    def check(message):
        return (
            message.author.id == interaction.user.id
            and message.channel.id == interaction.channel.id
        )

    try:
        return await interaction.client.wait_for(
            "message",
            timeout=timeout,
            check=check
        )

    except TimeoutError:
        await interaction.followup.send(
            "⏰ Reaction role setup timed out."
        )
        return None


# =========================================
# START SETUP
# =========================================

async def start_reaction_role_setup(
    interaction,
    channel
):

    await interaction.response.send_message(
        f"⚙️ Setting up reaction roles in {channel.mention}."
    )

    # =========================================
    # TITLE
    # =========================================

    title_message = await ask_message(
        interaction,
        "📝 What should the embed title be?"
    )

    if title_message is None:
        return

    if title_message.content.lower() == "cancel":
        await interaction.followup.send(
            "❌ Setup cancelled."
        )
        return

    title = title_message.content.strip()

    # =========================================
    # DESCRIPTION
    # =========================================

    description_message = await ask_message(
        interaction,
        "📖 What should the embed description be?"
    )

    if description_message is None:
        return

    if description_message.content.lower() == "cancel":
        await interaction.followup.send(
            "❌ Setup cancelled."
        )
        return

    description = description_message.content.strip()

    # =========================================
    # IMAGE
    # =========================================

    image_message = await ask_message(
        interaction,
        "🖼️ Upload an image or type `skip`."
    )

    if image_message is None:
        return

    if image_message.content.lower() == "cancel":
        await interaction.followup.send(
            "❌ Setup cancelled."
        )
        return

    image_url = None

    if image_message.attachments:

        image_url = image_message.attachments[0].url

    elif image_message.content.lower() != "skip":

        await interaction.followup.send(
            "❌ Please upload an image or type `skip`."
        )
        return

    # =========================================
    # COLOR
    # =========================================

    color_message = await ask_message(
        interaction,
        "🎨 What color should the embed be?\n"
        "Examples: `blue`, `gold`, `royalblue`, `#5865F2`"
    )

    if color_message is None:
        return

    if color_message.content.lower() == "cancel":
        await interaction.followup.send(
            "❌ Setup cancelled."
        )
        return

    color_value = parse_role_color(
        color_message.content
    )

    if color_value is None:

        await interaction.followup.send(
            "❌ Invalid color.\n"
            "Use a named color or a 6-digit hex color."
        )
        return

    color = discord.Color(
        color_value
    )

    # =========================================
    # REACTION ROLES
    # =========================================

    await interaction.followup.send(
        "🎭 **Reaction Roles**\n\n"
        "Send one reaction role per message.\n\n"
        "Example:\n"
        "🏴‍☠️ @Pirates\n"
        "⚓ @Marines\n"
        "🌊 @Civilians\n\n"
        "Type `done` when finished.\n"
        "Type `cancel` to cancel."
    )

    reaction_roles = []

    def role_check(message):

        return (
            message.author.id == interaction.user.id
            and message.channel.id == interaction.channel.id
        )

    while True:

        try:

            message = await interaction.client.wait_for(
                "message",
                timeout=300,
                check=role_check
            )

        except TimeoutError:

            await interaction.followup.send(
                "⏰ Reaction role setup timed out."
            )
            return

        # =========================================
        # CANCEL
        # =========================================

        if message.content.lower() == "cancel":

            await interaction.followup.send(
                "❌ Setup cancelled."
            )
            return

        # =========================================
        # DONE
        # =========================================

        if message.content.lower() == "done":
            break

        # =========================================
        # ROLE CHECK
        # =========================================

        if not message.role_mentions:

            await interaction.followup.send(
                "❌ You need to mention a role.\n"
                "Example: `🏴‍☠️ @Pirates`"
            )
            continue

        role = message.role_mentions[0]

        # =========================================
        # BOT ROLE CHECK
        # =========================================

        bot_member = interaction.guild.me

        if bot_member is None:

            await interaction.followup.send(
                "❌ I couldn't determine my server permissions."
            )
            continue

        if role >= bot_member.top_role:

            await interaction.followup.send(
                f"❌ I can't manage {role.mention}.\n"
                "My highest role must be above that role."
            )
            continue

        # =========================================
        # GET EMOJI
        # =========================================

        emoji = message.content

        for mentioned_role in message.role_mentions:

            emoji = emoji.replace(
                mentioned_role.mention,
                ""
            )

        emoji = emoji.strip()

        if not emoji:

            await interaction.followup.send(
                "❌ You need to include an emoji.\n"
                "Example: `🏴‍☠️ @Pirates`"
            )
            continue

        # =========================================
        # DUPLICATE EMOJI
        # =========================================

        if any(
            existing_emoji == emoji
            for existing_emoji, _ in reaction_roles
        ):

            await interaction.followup.send(
                f"❌ {emoji} is already being used."
            )
            continue

        # =========================================
        # ADD REACTION ROLE
        # =========================================

        reaction_roles.append(
            (
                emoji,
                role
            )
        )

        await interaction.followup.send(
            f"✅ Added {emoji} → {role.mention}"
        )

    # =========================================
    # CHECK ROLES
    # =========================================

    if not reaction_roles:

        await interaction.followup.send(
            "❌ No reaction roles were added."
        )
        return

    # =========================================
    # ROLE LIST
    # =========================================

    role_lines = "\n".join(
        f"{emoji} — {role.mention}"
        for emoji, role in reaction_roles
    )

    # =========================================
    # CREATE EMBED
    # =========================================

    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )

    embed.add_field(
        name="🎭 Reaction Roles",
        value=role_lines,
        inline=False
    )

    if image_url:

        embed.set_image(
            url=image_url
        )

    embed.set_footer(
        text="React below to get your role!"
    )

    # =========================================
    # SEND PANEL
    # =========================================

    try:

        panel = await channel.send(
            embed=embed
        )

    except discord.Forbidden:

        await interaction.followup.send(
            "❌ I don't have permission to send messages "
            f"in {channel.mention}."
        )
        return

    except discord.HTTPException:

        await interaction.followup.send(
            "❌ Discord rejected the panel message."
        )
        return

    # =========================================
    # ADD REACTIONS
    # =========================================

    successful_roles = []

    for emoji, role in reaction_roles:

        try:

            await panel.add_reaction(
                emoji
            )

            successful_roles.append(
                (
                    emoji,
                    role
                )
            )

        except discord.HTTPException:

            await interaction.followup.send(
                f"⚠️ I couldn't add the {emoji} reaction."
            )

    # =========================================
    # SAVE TO DATABASE
    # =========================================

    for emoji, role in successful_roles:

        db.insert(
            "reaction_roles",
            "guild_id, message_id, emoji, role_id",
            (
                interaction.guild.id,
                panel.id,
                emoji,
                role.id
            )
        )

    # =========================================
    # FINISHED
    # =========================================

    await interaction.followup.send(
        f"✅ Reaction role panel created in {channel.mention}!"
    )


# =========================================
# SETUP
# =========================================

def setup(bot):

    # =========================================
    # ADD ROLE
    # =========================================

    async def on_raw_reaction_add(payload):

        if payload.guild_id is None:
            return

        if payload.user_id == bot.user.id:
            return

        reaction_role = db.fetchone(
            "reaction_roles",
            "message_id = ? AND emoji = ?",
            (
                payload.message_id,
                str(payload.emoji)
            )
        )

        if reaction_role is None:
            return

        guild = bot.get_guild(
            payload.guild_id
        )

        if guild is None:
            return

        member = guild.get_member(
            payload.user_id
        )

        if member is None:
            return

        if member.bot:
            return

        role = guild.get_role(
            reaction_role[3]
        )

        if role is None:
            return

        try:

            await member.add_roles(
                role
            )

        except discord.Forbidden:
            return

    # =========================================
    # REMOVE ROLE
    # =========================================

    async def on_raw_reaction_remove(payload):

        if payload.guild_id is None:
            return

        reaction_role = db.fetchone(
            "reaction_roles",
            "message_id = ? AND emoji = ?",
            (
                payload.message_id,
                str(payload.emoji)
            )
        )

        if reaction_role is None:
            return

        guild = bot.get_guild(
            payload.guild_id
        )

        if guild is None:
            return

        member = guild.get_member(
            payload.user_id
        )

        if member is None:
            return

        if member.bot:
            return

        role = guild.get_role(
            reaction_role[3]
        )

        if role is None:
            return

        try:

            await member.remove_roles(
                role
            )

        except discord.Forbidden:
            return

    # =========================================
    # REGISTER LISTENERS
    # =========================================

    bot.add_listener(
        on_raw_reaction_add
    )

    bot.add_listener(
        on_raw_reaction_remove
    )