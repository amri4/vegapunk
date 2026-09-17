import asyncio

import discord


TIMEOUT = 300


async def ask_question(
    channel,
    user,
    question
):
    await channel.send(question)

    def check(message):
        return (
            message.author.id == user.id
            and message.channel.id == channel.id
        )

    try:
        return await channel.guild._state._get_client().wait_for(
            "message",
            check=check,
            timeout=TIMEOUT
        )
    except asyncio.TimeoutError:
        return None


async def start_embed_setup(
    interaction: discord.Interaction,
    target_channel: discord.TextChannel
):
    user = interaction.user
    channel = interaction.channel

    await interaction.response.send_message(
        "📝 Embed setup started."
    )

    title_message = await ask_question(
        channel,
        user,
        "What should the **title** be? Type `skip` to leave it empty."
    )

    if title_message is None:
        await channel.send("⌛ Embed setup timed out.")
        return

    title = None if title_message.content.lower() == "skip" else title_message.content

    description_message = await ask_question(
        channel,
        user,
        "What should the **description** be? Type `skip` to leave it empty."
    )

    if description_message is None:
        await channel.send("⌛ Embed setup timed out.")
        return

    description = (
        None
        if description_message.content.lower() == "skip"
        else description_message.content
    )

    color_message = await ask_question(
        channel,
        user,
        "What color should the embed use? Use a hex color like `#ff0000`, or type `skip`."
    )

    if color_message is None:
        await channel.send("⌛ Embed setup timed out.")
        return

    color = None if color_message.content.lower() == "skip" else color_message.content

    await channel.send(
        "🖼️ **Image:** Upload an image, or type `skip`."
    )

    def image_check(message):
        return (
            message.author.id == user.id
            and message.channel.id == channel.id
        )

    try:
        image_message = await interaction.client.wait_for(
            "message",
            check=image_check,
            timeout=TIMEOUT
        )
    except asyncio.TimeoutError:
        await channel.send("⌛ Embed setup timed out.")
        return

    image = None

    if image_message.content.lower() != "skip":
        if image_message.attachments:
            image = image_message.attachments[0].url
        else:
            await channel.send(
                "❌ Please upload an image or type `skip`."
            )
            return

    await channel.send(
        "🖼️ **Thumbnail:** Upload an image, or type `skip`."
    )

    try:
        thumbnail_message = await interaction.client.wait_for(
            "message",
            check=image_check,
            timeout=TIMEOUT
        )
    except asyncio.TimeoutError:
        await channel.send("⌛ Embed setup timed out.")
        return

    thumbnail = None

    if thumbnail_message.content.lower() != "skip":
        if thumbnail_message.attachments:
            thumbnail = thumbnail_message.attachments[0].url
        else:
            await channel.send(
                "❌ Please upload an image or type `skip`."
            )
            return

    embed = discord.Embed(
        title=title,
        description=description
    )

    if color:
        try:
            color_value = color.replace("#", "")
            embed.color = discord.Color(
                int(color_value, 16)
            )
        except ValueError:
            await channel.send(
                "❌ Invalid color. Embed was not sent."
            )
            return

    if image:
        embed.set_image(url=image)

    if thumbnail:
        embed.set_thumbnail(url=thumbnail)

    embed.set_footer(
        text=interaction.guild.name
    )

    await target_channel.send(
        embed=embed
    )

    await channel.send(
        f"✅ Embed sent to {target_channel.mention}."
    )