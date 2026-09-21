import discord

from ..functions.trades import get_trade
from ..functions.offer import remove_item_from_trade
from ..functions.berries import remove_berries_from_trade


class RemoveItemModal(discord.ui.Modal):
    def __init__(self, trade_id):
        super().__init__(
            title="Remove from Trade"
        )

        self.trade_id = trade_id

        self.item_id = discord.ui.TextInput(
            label="Item ID",
            placeholder="Example: gomu_gomu or berries",
            required=True,
            max_length=100
        )

        self.amount = discord.ui.TextInput(
            label="Amount",
            placeholder="How many?",
            required=True,
            min_length=1,
            max_length=10
        )

        self.add_item(
            self.item_id
        )

        self.add_item(
            self.amount
        )

    async def on_submit(
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
                "❌ This trade isn't open for offers.",
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

        try:
            amount = int(
                self.amount.value
            )
        except ValueError:
            await interaction.response.send_message(
                "❌ Amount must be a whole number.",
                ephemeral=True
            )
            return

        if amount <= 0:
            await interaction.response.send_message(
                "❌ Amount must be greater than 0.",
                ephemeral=True
            )
            return

        item_id = self.item_id.value.strip()

        if item_id.lower() == "berries":
            success = remove_berries_from_trade(
                self.trade_id,
                interaction.user.id,
                amount
            )
        else:
            success = remove_item_from_trade(
                self.trade_id,
                interaction.user.id,
                item_id,
                amount
            )

        if not success:
            await interaction.response.send_message(
                "❌ You aren't offering that amount.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"✅ Removed **{item_id} ×{amount}** "
            f"from the trade.",
            ephemeral=True
        )