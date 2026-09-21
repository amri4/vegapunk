import discord

from ..modals.add import AddItemModal


class AddItemButton(discord.ui.Button):
    def __init__(self, trade_id):
        super().__init__(
            label="Add Item",
            style=discord.ButtonStyle.primary,
            custom_id=f"trade:add:{trade_id}"
        )

        self.trade_id = trade_id

    async def callback(
        self,
        interaction: discord.Interaction
    ):
        await interaction.response.send_modal(
            AddItemModal(self.trade_id)
        )