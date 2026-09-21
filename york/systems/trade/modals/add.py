import discord

from ..functions.trades import get_trade
from ..functions.offer import add_item_to_trade
from ..functions.berries import add_berries_to_trade
from ..functions.message import update_trade_message


class AddItemModal(discord.ui.Modal):
    def __init__(self, trade_id):
        super().__init__(
            title="Add to Trade"
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

        if not item_id:
            await interaction.response.send_message(
                "❌ Enter an item ID.",
                ephemeral=True
            )
            return

        if item_id.lower() == "berries":
            success = add_berries_to_trade(
                self.trade_id,
                trade[1],
                interaction.user.id,
                amount
            )
        else:
            success = add_item_to_trade(
                self.trade_id,
                trade[1],
                interaction.user.id,
                item_id,
                amount
            )

        if not success:
            await interaction.response.send_message(
                "❌ You don't have enough of that item.",
                ephemeral=True
            )
            return

        await update_trade_message(
            interaction.message,
            self.trade_id
        )

        await interaction.response.send_message(
            f"✅ Added **{item_id} ×{amount}** "
            f"to the trade.",
            ephemeral=True
        )