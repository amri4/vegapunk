import discord

from ..functions.trades import (
    get_trade,
    update_trade_status
)

from ..functions.confirmations import (
    confirm_trade,
    is_confirmed,
    get_confirmations,
    clear_confirmations
)

from ..functions.complete import complete_trade
from ..functions.offers import remove_offers


class ConfirmTradeButton(discord.ui.Button):
    def __init__(self, trade_id):
        super().__init__(
            label="Confirm",
            style=discord.ButtonStyle.success,
            custom_id=f"trade:confirm:{trade_id}"
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

        if trade[4] != "accepted":
            await interaction.response.send_message(
                "❌ This trade is no longer active.",
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
                "✅ You confirmed the trade.\n"
                "Waiting for the other person.",
                ephemeral=True
            )
            return

        completed = complete_trade(
            trade
        )

        if not completed:
            clear_confirmations(
                self.trade_id
            )

            await interaction.response.send_message(
                "❌ The trade could not be completed.\n"
                "One or more offered items are no longer available.",
                ephemeral=True
            )
            return

        update_trade_status(
            self.trade_id,
            "completed"
        )

        clear_confirmations(
            self.trade_id
        )

        remove_offers(
            self.trade_id
        )

        await interaction.response.edit_message(
            content=f"✅ Trade **#{self.trade_id}** completed!",
            embed=None,
            view=None
        )