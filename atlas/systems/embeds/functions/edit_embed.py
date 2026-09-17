import discord


async def edit_embed(
    interaction: discord.Interaction,
    message_id: str,
    title: str | None,
    description: str | None,
    color: str | None,
    image: discord.Attachment | None,
    thumbnail: discord.Attachment | None
):
    try:
        message_id = int(message_id)
    except ValueError:
        await interaction.response.send_message(
            "❌ Invalid message ID."
        )
        return

    message = None

    for channel in interaction.guild.text_channels:
        try:
            message = await channel.fetch_message(message_id)
            break
        except discord.NotFound:
            continue
        except discord.Forbidden:
            continue

    if message is None:
        await interaction.response.send_message(
            "❌ I couldn't find that message."
        )
        return

    if not message.embeds:
        await interaction.response.send_message(
            "❌ That message doesn't contain an embed."
        )
        return

    embed = message.embeds[0]

    if title is not None:
        embed.title = title

    if description is not None:
        embed.description = description

    if color is not None:
        try:
            color_value = color.replace("#", "")
            embed.color = discord.Color(
                int(color_value, 16)
            )
        except ValueError:
            await interaction.response.send_message(
                "❌ Invalid color."
            )
            return

    if image is not None:
        embed.set_image(
            url=image.url
        )

    if thumbnail is not None:
        embed.set_thumbnail(
            url=thumbnail.url
        )

    embed.set_footer(
        text=interaction.guild.name
    )

    await message.edit(
        embed=embed
    )

    await interaction.response.send_message(
        "✅ Embed updated."
    )