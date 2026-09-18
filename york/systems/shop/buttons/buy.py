import discord

from ..functions.shop import get_item
from ..views.confirm import ConfirmView, confirmation_embed


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

        view = ConfirmView(
            self.item_id,
            interaction.user.id
        )

        await interaction.response.send_message(
            embed=confirmation_embed(item),
            view=view,
            ephemeral=True
        )