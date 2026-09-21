import discord

from ..functions.trades import get_trade
from ..functions.offers import get_offer, remove_offer


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

        offer = get_offer(
            self.trade_id,
            interaction.user.id,
            item_id
        )

        if offer is None:
            await interaction.response.send_message(
                "❌ You aren't offering that item.",
                ephemeral=True
            )
            return

        offered_amount = offer[3]

        if amount > offered_amount:
            await interaction.response.send_message(
                f"❌ You're only offering **{offered_amount:,}** "
                f"of that item.",
                ephemeral=True
            )
            return

        if amount == offered_amount:
            remove_offer(
                self.trade_id,
                interaction.user.id,
                item_id
            )
        else:
            from ..functions.offers import update_offer

            update_offer(
                self.trade_id,
                interaction.user.id,
                item_id,
                offered_amount - amount
            )

        await interaction.response.send_message(
            f"✅ Removed **{item_id} ×{amount}** "
            f"from the trade.",
            ephemeral=True
        )