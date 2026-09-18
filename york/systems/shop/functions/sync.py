import discord

from ..items import SHOP_ITEMS
from .shop import (
    add_item,
    get_item,
    get_items,
    get_shop_channel,
    remove_item,
    update_message_id
)
from ..views.shop import ShopView


async def sync_shop(bot, guild):
    channel_id = get_shop_channel(
        guild.id
    )

    if channel_id is None:
        return False

    channel = guild.get_channel(
        channel_id
    )

    if channel is None:
        return False

    current_item_ids = {
        item["id"]
        for item in SHOP_ITEMS
    }

    saved_items = get_items(
        guild.id
    )

    for saved in saved_items:
        item_id = saved[0]

        if item_id == "__channel__":
            continue

        if item_id in current_item_ids:
            continue

        try:
            message = await channel.fetch_message(
                saved[3]
            )

            await message.delete()

        except discord.NotFound:
            pass

        remove_item(
            item_id,
            guild.id
        )

    for item in SHOP_ITEMS:
        saved = get_item(
            item["id"],
            guild.id
        )

        embed = discord.Embed(
            title=item["title"],
            description=(
                f"{item['description']}\n\n"
                f"**Price:** {item['price']:,} 🍓"
            )
        )

        view = ShopView(
            item
        )

        if saved is None:
            message = await channel.send(
                embed=embed,
                view=view
            )

            add_item(
                item["id"],
                guild.id,
                channel.id,
                message.id
            )

            continue

        try:
            message = await channel.fetch_message(
                saved[3]
            )

        except discord.NotFound:
            message = await channel.send(
                embed=embed,
                view=view
            )

            update_message_id(
                item["id"],
                guild.id,
                message.id
            )

            continue

        await message.edit(
            embed=embed,
            view=view
        )

    return True