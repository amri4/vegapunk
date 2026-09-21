import discord

from ..functions.trades import get_trade
from ..functions.confirmations import (
    confirm_trade,
    is_confirmed,
    get_confirmations
)


class ConfirmTradeButton(discord.ui.Button):
    def __init__(self, trade_id):
        super().__init__(
            label="Confirm",
            style=discord.ButtonStyle.success
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
                "❌ This trade doesn't exist.",
                ephemeral=True
            )
            return

        if trade[4] != "accepted":
            await interaction.response.send_message(
                "❌ This trade isn't open.",
                ephemeral=True
            )
            return

        if interaction.user.id not in (
            trade[2],
            trade[3]
        ):
            await interaction.response.send_message(
                "❌ You aren't part of this trade.",
                ephemeral=True
            )
            return

        if is_confirmed(
            self.trade_id,
            interaction.user.id
        ):
            await interaction.response.send_message(
                "❌ You already confirmed this trade.",
                ephemeral=True
            )
            return

        confirm_trade(
            self.trade_id,
            interaction.user.id
        )

        confirmations = get_confirmations(
            self.trade_id
        )

        if len(confirmations) < 2:
            await interaction.response.send_message(
                "✅ You confirmed the trade. "
                "Waiting for the other person.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            "✅ Both users confirmed! "
            "The trade is ready to be completed.",
            ephemeral=True
        )