import discord

from ..views.confirm import ConfirmView, confirmation_embed
from ..modals.bounty import BountyModal


class BuyButton(discord.ui.Button):
    def __init__(self, item):
        super().__init__(
            label="Buy",
            style=discord.ButtonStyle.success,
            custom_id=f"shop_buy:{item['id']}"
        )

        self.item = item

    async def callback(self, interaction):
        if self.item.get("type") == "variable":
            await interaction.response.send_modal(
                BountyModal(self.item)
            )
            return

        view = ConfirmView(
            self.item,
            interaction.user.id
        )

        await interaction.response.send_message(
            embed=confirmation_embed(self.item),
            view=view,
            ephemeral=True
        )