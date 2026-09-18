import discord

from ..items import SHOP_ITEMS
from .shop import (
    add_item,
    get_item,
    get_items,
    remove_item,
    update_message_id
)
from ..views.shop import ShopView


async def sync_shop(bot):
    current_item_ids = {
        item["id"]
        for item in SHOP_ITEMS
    }

    saved_items = get_items()

    # Remove items that no longer exist in items.py
    for saved in saved_items:
        item_id = saved[0]

        if item_id in current_item_ids:
            continue

        channel = bot.get_channel(saved[1])

        if channel is not None:
            try:
                message = await channel.fetch_message(
                    saved[2]
                )

                await message.delete()

            except discord.NotFound:
                pass

        remove_item(
            item_id
        )

    # Create or update current items
    for item in SHOP_ITEMS:
        saved = get_item(
            item["id"]
        )

        channel = bot.get_channel(
            item["channel_id"]
        )

        if channel is None:
            continue

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
                channel.id,
                message.id
            )

            continue

        message_id = saved[2]

        try:
            message = await channel.fetch_message(
                message_id
            )

        except discord.NotFound:
            message = await channel.send(
                embed=embed,
                view=view
            )

            update_message_id(
                item["id"],
                message.id
            )

            continue

        await message.edit(
            embed=embed,
            view=view
        )


async def setup(bot):
    await sync_shop(bot)