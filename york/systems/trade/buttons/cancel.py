import discord

from ..functions.trades import (
    get_trade,
    update_trade_status
)

from ..functions.confirmations import clear_confirmations
from ..functions.offers import remove_offers


class CancelTradeButton(discord.ui.Button):
    def __init__(self, trade_id):
        super().__init__(
            label="Cancel",
            style=discord.ButtonStyle.danger,
            custom_id=f"trade:cancel:{trade_id}"
        )

        self.trade_id = trade_id

    async def callback(
        self,
        interaction: discord.Interaction
    ):
        trade = get_trade(
            self.trade_id
        )

        if trade is None:
            await interaction.response.send_message(
                "❌ This trade no longer exists.",
                ephemeral=True
            )
            return

        if trade[4] not in (
            "pending",
            "accepted"
        ):
            await interaction.response.send_message(
                "❌ This trade can no longer be cancelled.",
                ephemeral=True
            )
            return

        if interaction.user.id not in (
            trade[2],
            trade[3]
        ):
            await interaction.response.send_message(
                "❌ You are not part of this trade.",
                ephemeral=True
            )
            return

        update_trade_status(
            self.trade_id,
            "cancelled"
        )

        clear_confirmations(
            self.trade_id
        )

        remove_offers(
            self.trade_id
        )

        await interaction.response.edit_message(
            content=f"❌ Trade **#{self.trade_id}** cancelled.",
            embed=None,
            view=None
        )