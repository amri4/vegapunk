import discord
import mycord

db = mycord.DB()


async def ask_message(interaction, question, timeout=300):
    await interaction.followup.send(question)

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
            "⏰ Setup timed out."
        )
        return None


async def start_reaction_role_setup(interaction, channel):
    await interaction.response.send_message(
        f"Let's set up reaction roles for {channel.mention}."
    )

    title_message = await ask_message(
        interaction,
        "📝 What should the embed title be?"
    )
    if title_message is None:
        return

    title = title_message.content

    description_message = await ask_message(
        interaction,
        "📖 What should the embed description be?"
    )
    if description_message is None:
        return

    description = description_message.content

    image_message = await ask_message(
        interaction,
        "🖼️ Upload an image or type `skip`."
    )
    if image_message is None:
        return

    image_url = None

    if image_message.attachments:
        image_url = image_message.attachments[0].url
    elif image_message.content.lower() != "skip":
        await interaction.followup.send(
            "❌ Please upload an image or type `skip`."
        )
        return

    color_message = await ask_message(
        interaction,
        "🎨 What color should the embed be? Example: `#5865F2`"
    )
    if color_message is None:
        return

    try:
        color = discord.Color.from_str(color_message.content)
    except ValueError:
        await interaction.followup.send(
            "❌ Invalid hex color."
        )
        return

    await interaction.followup.send(
        "🎭 Send your reaction roles one at a time.\n"
        "Example: `🏴‍☠️ @Pirates`\n"
        "Type `done` when finished."
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
                "⏰ Setup timed out."
            )
            return

        if message.content.lower() == "done":
            break

        if message.content.lower() == "cancel":
            await interaction.followup.send(
                "❌ Reaction role setup cancelled."
            )
            return

        if not message.role_mentions:
            await interaction.followup.send(
                "❌ Please include a role mention.\n"
                "Example: `🏴‍☠️ @Pirates`"
            )
            continue

        role = message.role_mentions[0]

        if role >= interaction.guild.me.top_role:
            await interaction.followup.send(
                f"❌ I can't manage {role.mention}. "
                "My highest role must be above it."
            )
            continue

        content_without_role = message.content.replace(
            role.mention,
            ""
        ).strip()

        emoji = content_without_role

        if not emoji:
            await interaction.followup.send(
                "❌ Please include an emoji before the role."
            )
            continue

        reaction_roles.append((emoji, role))

        await interaction.followup.send(
            f"✅ Added {emoji} → {role.mention}"
        )

    if not reaction_roles:
        await interaction.followup.send(
            "❌ You didn't add any reaction roles."
        )
        return

    role_lines = "\n".join(
        f"{emoji} — {role.mention}"
        for emoji, role in reaction_roles
    )

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
        embed.set_image(url=image_url)

    embed.set_footer(
        text="React below to get your role!"
    )

    panel = await channel.send(embed=embed)

    for emoji, role in reaction_roles:
        try:
            await panel.add_reaction(emoji)

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
        except Exception:
            continue

    await interaction.followup.send(
        f"✅ Reaction role panel created in {channel.mention}!"
    )


def setup(bot):

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

        guild = bot.get_guild(payload.guild_id)

        if guild is None:
            return

        member = guild.get_member(payload.user_id)

        if member is None or member.bot:
            return

        role = guild.get_role(reaction_role[3])

        if role is None:
            return

        try:
            await member.add_roles(role)
        except discord.Forbidden:
            pass

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

        guild = bot.get_guild(payload.guild_id)

        if guild is None:
            return

        member = guild.get_member(payload.user_id)

        if member is None or member.bot:
            return

        role = guild.get_role(reaction_role[3])

        if role is None:
            return

        try:
            await member.remove_roles(role)
        except discord.Forbidden:
            pass

    bot.add_listener(on_raw_reaction_add)
    bot.add_listener(on_raw_reaction_remove)