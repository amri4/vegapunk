import discord

from ..functions.shop import get_item


class BuyButton(discord.ui.Button):
    def __init__(
        self,
        item_id
    ):
        super().__init__(
            label="Buy",
            style=discord.ButtonStyle.success,
            custom_id=f"shop_buy:{item_id}"
        )

        self.item_id = item_id

    async def callback(
        self,
        interaction: discord.Interaction
    ):
        item = get_item(
            self.item_id
        )

        if item is None:
            await interaction.response.send_message(
                "❌ This item no longer exists.",
                ephemeral=True
            )
            return

        title = item[1]
        price = item[3]

        await interaction.response.send_message(
            f"🛒 You selected **{title}** for **{price:,} 🍓**.",
            ephemeral=True
        )