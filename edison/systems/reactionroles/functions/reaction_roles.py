import asyncio

import discord
import mycord


db = mycord.DB()


async def ask_message(interaction, question, timeout=300):
    await interaction.followup.send(
        question,
        ephemeral=True
    )

    def check(message):
        return (
            message.author.id == interaction.user.id
            and message.channel.id == interaction.channel.id
        )

    try:
        return await interaction.client.wait_for(
            "message",
            check=check,
            timeout=timeout
        )

    except asyncio.TimeoutError:
        await interaction.followup.send(
            "⌛ Reaction role setup timed out.",
            ephemeral=True
        )
        return None


async def start_reaction_role_setup(interaction, channel):
    if interaction.guild is None:
        return await interaction.response.send_message(
            "❌ This command can only be used in a server.",
            ephemeral=True
        )

    await interaction.response.send_message(
        f"🎭 **Reaction Role Setup**\n\n"
        f"Panel channel: {channel.mention}\n\n"
        "Let's set everything up.",
        ephemeral=True
    )

    # TITLE
    message = await ask_message(
        interaction,
        "📝 **What should the title be?**"
    )

    if message is None:
        return

    if message.content.lower() == "cancel":
        return await interaction.followup.send(
            "❌ Setup cancelled.",
            ephemeral=True
        )

    title = message.content.strip()

    # DESCRIPTION
    message = await ask_message(
        interaction,
        "📄 **What should the description be?**"
    )

    if message is None:
        return

    if message.content.lower() == "cancel":
        return await interaction.followup.send(
            "❌ Setup cancelled.",
            ephemeral=True
        )

    description = message.content.strip()

    # IMAGE
    message = await ask_message(
        interaction,
        "🖼️ **Upload an image for the embed, or type `skip`.**"
    )

    if message is None:
        return

    if message.content.lower() == "cancel":
        return await interaction.followup.send(
            "❌ Setup cancelled.",
            ephemeral=True
        )

    image_url = None

    if message.content.lower() != "skip":
        if not message.attachments:
            await interaction.followup.send(
                "❌ Please upload an image or type `skip`.",
                ephemeral=True
            )

            message = await ask_message(
                interaction,
                "🖼️ Upload an image or type `skip`."
            )

            if message is None:
                return

        if message.content.lower() == "skip":
            image_url = None

        elif message.attachments:
            image_url = message.attachments[0].url

        else:
            await interaction.followup.send(
                "❌ No image was uploaded. Setup cancelled.",
                ephemeral=True
            )
            return

    else:
        image_url = None

    # COLOR
    message = await ask_message(
        interaction,
        "🎨 **What color should the embed use?**\n"
        "Use a hex color such as `#5865F2`."
    )

    if message is None:
        return

    if message.content.lower() == "cancel":
        return await interaction.followup.send(
            "❌ Setup cancelled.",
            ephemeral=True
        )

    color_text = message.content.strip()

    if color_text.startswith("#"):
        color_text = color_text[1:]

    try:
        color = discord.Color(int(color_text, 16))
    except ValueError:
        return await interaction.followup.send(
            "❌ That's not a valid hex color.",
            ephemeral=True
        )

    # REACTION ROLES
    await interaction.followup.send(
        "🎭 **Now add your reaction roles.**\n\n"
        "Send them like:\n"
        "`🏴‍☠️ @Pirates`\n"
        "`⚓ @Marines`\n\n"
        "You can add as many as you want.\n"
        "Type **`done`** when you're finished.",
        ephemeral=True
    )

    reaction_roles = []

    def reaction_check(message):
        return (
            message.author.id == interaction.user.id
            and message.channel.id == interaction.channel.id
        )

    while True:
        try:
            message = await interaction.client.wait_for(
                "message",
                check=reaction_check,
                timeout=300
            )
        except asyncio.TimeoutError:
            await interaction.followup.send(
                "⌛ Reaction role setup timed out.",
                ephemeral=True
            )
            return

        content = message.content.strip()

        if content.lower() == "cancel":
            await interaction.followup.send(
                "❌ Setup cancelled.",
                ephemeral=True
            )
            return

        if content.lower() == "done":
            break

        if not message.role_mentions:
            await message.reply(
                "❌ Please include a role mention.\n"
                "Example: `🏴‍☠️ @Pirates`"
            )
            continue

        role = message.role_mentions[0]

        if role >= interaction.guild.me.top_role:
            await message.reply(
                "❌ I can't give that role because it is higher "
                "than or equal to my highest role."
            )
            continue

        emoji = content

        # Remove the role mention from the message.
        emoji = emoji.replace(role.mention, "").strip()

        if not emoji:
            await message.reply(
                "❌ You need to provide an emoji."
            )
            continue

        if any(
            existing_emoji == emoji
            for existing_emoji, existing_role in reaction_roles
        ):
            await message.reply(
                "❌ That emoji is already being used."
            )
            continue

        reaction_roles.append(
            (emoji, role)
        )

        await message.reply(
            f"✅ Added {emoji} → {role.mention}"
        )

    if not reaction_roles:
        return await interaction.followup.send(
            "❌ You didn't add any reaction roles.",
            ephemeral=True
        )

    # CREATE EMBED
    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )

    if image_url:
        embed.set_image(
            url=image_url
        )

    embed.set_footer(
        text=f"Reaction roles • {interaction.guild.name}"
    )

    # SEND PANEL
    panel_message = await channel.send(
        embed=embed
    )

    # ADD REACTIONS + SAVE
    for emoji, role in reaction_roles:
        try:
            await panel_message.add_reaction(
                emoji
            )
        except discord.HTTPException:
            continue

        db.insert(
            "reaction_roles",
            "guild_id, message_id, emoji, role_id",
            (
                interaction.guild.id,
                panel_message.id,
                emoji,
                role.id
            )
        )

    await interaction.followup.send(
        f"✅ **Reaction role panel created!**\n"
        f"📍 {channel.mention}",
        ephemeral=True
    )


async def on_raw_reaction_add(payload):
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

    guild = discord.utils.get(
        payload.member.guilds if payload.member else [],
        id=payload.guild_id
    )

    if guild is None:
        return

    role = guild.get_role(
        reaction_role[3]
    )

    if role is None:
        return

    member = guild.get_member(
        payload.user_id
    )

    if member is None or member.bot:
        return

    await member.add_roles(role)


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

    guild = payload.guild

    if guild is None:
        return

    member = guild.get_member(
        payload.user_id
    )

    if member is None or member.bot:
        return

    role = guild.get_role(
        reaction_role[3]
    )

    if role is None:
        return

    await member.remove_roles(role)


def setup(bot):
    bot.add_listener(on_raw_reaction_add)
    bot.add_listener(on_raw_reaction_remove)