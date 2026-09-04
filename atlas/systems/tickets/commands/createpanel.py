import asyncio

import discord
from discord.ext import commands

import mycord


db = mycord.PunksDB()


# =========================================
# WAIT FOR USER RESPONSE
# =========================================

async def wait_for_response(ctx):

    def check(message):

        return (
            message.author == ctx.author
            and message.channel == ctx.channel
        )

    try:

        return await ctx.bot.wait_for(
            "message",
            check=check,
            timeout=300
        )

    except asyncio.TimeoutError:

        await ctx.send(
            "⌛ Panel setup timed out."
        )

        return None


# =========================================
# GET IMAGE
# =========================================

async def get_image(ctx, message):

    if message.content.lower() == "skip":
        return None

    if not message.attachments:

        await ctx.send(
            "❌ Please upload an image or type `skip`."
        )

        return False

    attachment = message.attachments[0]

    if attachment.content_type:

        if not attachment.content_type.startswith(
            "image/"
        ):

            await ctx.send(
                "❌ That attachment isn't an image. "
                "Please upload an image or type `skip`."
            )

            return False

    return attachment.url


# =========================================
# CREATE PANEL
# =========================================

@commands.command(
    name="createpanel",
    help="Create a ticket panel."
)
async def createpanel(ctx):

    if ctx.guild is None:

        await ctx.send(
            "❌ This command can only be used in a server."
        )

        return

    # =====================================
    # GET PANEL CHANNEL
    # =====================================

    config = db.fetchone(
        "server_config",
        "guild_id = ?",
        (ctx.guild.id,)
    )

    if not config:

        await ctx.send(
            "❌ This server hasn't been configured yet."
        )

        return

    # server_config:
    # 0 = guild_id
    # 1 = member_role_id
    # 2 = verification_channel_id
    # 3 = verification_enabled
    # 4 = ticket_panel_channel_id

    ticket_panel_channel_id = config[4]

    if not ticket_panel_channel_id:

        await ctx.send(
            "❌ No ticket panel channel has been configured."
        )

        return

    panel_channel = ctx.guild.get_channel(
        ticket_panel_channel_id
    )

    if panel_channel is None:

        await ctx.send(
            "❌ The configured ticket panel channel no longer exists."
        )

        return

    # =====================================
    # TITLE
    # =====================================

    await ctx.send(
        "🎫 What should the panel title be?\n"
        "Type `cancel` to stop."
    )

    response = await wait_for_response(ctx)

    if response is None:
        return

    if response.content.lower() == "cancel":

        await ctx.send("❌ Panel setup cancelled.")

        return

    title = response.content

    # =====================================
    # DESCRIPTION
    # =====================================

    await ctx.send(
        "📝 What should the panel description be?"
    )

    response = await wait_for_response(ctx)

    if response is None:
        return

    if response.content.lower() == "cancel":

        await ctx.send("❌ Panel setup cancelled.")

        return

    description = response.content

    # =====================================
    # PANEL IMAGE
    # =====================================

    await ctx.send(
        "🖼️ Upload a panel image, or type `skip`."
    )

    while True:

        response = await wait_for_response(ctx)

        if response is None:
            return

        if response.content.lower() == "cancel":

            await ctx.send("❌ Panel setup cancelled.")

            return

        image_url = await get_image(
            ctx,
            response
        )

        if image_url is False:
            continue

        break

    # =====================================
    # THUMBNAIL
    # =====================================

    await ctx.send(
        "🖼️ Upload a thumbnail, or type `skip`."
    )

    while True:

        response = await wait_for_response(ctx)

        if response is None:
            return

        if response.content.lower() == "cancel":

            await ctx.send("❌ Panel setup cancelled.")

            return

        thumbnail_url = await get_image(
            ctx,
            response
        )

        if thumbnail_url is False:
            continue

        break

    # =====================================
    # CREATE EMBED
    # =====================================

    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.blue()
    )

    if image_url:
        embed.set_image(
            url=image_url
        )

    if thumbnail_url:
        embed.set_thumbnail(
            url=thumbnail_url
        )

    # =====================================
    # POST PANEL
    # =====================================

    try:

        panel_message = await panel_channel.send(
            embed=embed
        )

    except discord.Forbidden:

        await ctx.send(
            "❌ I don't have permission to send messages "
            "in the configured ticket panel channel."
        )

        return

    except discord.HTTPException:

        await ctx.send(
            "❌ Discord couldn't post the ticket panel."
        )

        return

    # =====================================
    # SAVE PANEL
    # =====================================

    try:

        db.insert(
            "ticket_panels",
            """
            guild_id,
            message_id,
            title,
            description,
            image_url,
            thumbnail_url
            """,
            (
                ctx.guild.id,
                panel_message.id,
                title,
                description,
                image_url,
                thumbnail_url
            )
        )

    except Exception as error:

        # Remove the Discord message so we
        # don't leave an unsaved panel behind.

        try:
            await panel_message.delete()
        except Exception:
            pass

        await ctx.send(
            f"❌ Failed to save the ticket panel: `{error}`"
        )

        return

    await ctx.send(
        f"✅ Ticket panel created in {panel_channel.mention}."
    )


def setup(bot):

    bot.add_command(
        createpanel
    )