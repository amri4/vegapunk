import discord

from ..modals.remove import RemoveItemModal


class RemoveItemButton(discord.ui.Button):
    def __init__(self, trade_id):
        super().__init__(
            label="Remove Item",
            style=discord.ButtonStyle.secondary
        )

        self.trade_id = trade_id

    async def callback(
        self,
        interaction: discord.Interaction
    ):
        await interaction.response.send_modal(
            RemoveItemModal(
                self.trade_id
            )
        )