import discord

from ..functions.trades import (
    get_trade,
    update_trade_status
)

from ..views.trade import TradeView


class AcceptTradeButton(discord.ui.Button):
    def __init__(self, trade_id):
        super().__init__(
            label="Accept",
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
                "❌ This trade no longer exists.",
                ephemeral=True
            )
            return

        if trade[4] != "pending":
            await interaction.response.send_message(
                "❌ This trade is no longer pending.",
                ephemeral=True
            )
            return

        if interaction.user.id != trade[3]:
            await interaction.response.send_message(
                "❌ You are not the recipient of this trade.",
                ephemeral=True
            )
            return

        update_trade_status(
            self.trade_id,
            "accepted"
        )

        view = TradeView(
            self.trade_id
        )

        await interaction.response.edit_message(
            content=(
                f"🤝 Trade **#{self.trade_id}** accepted!\n"
                "Add what you want to offer below."
            ),
            view=view
        )


class DeclineTradeButton(discord.ui.Button):
    def __init__(self, trade_id):
        super().__init__(
            label="Decline",
            style=discord.ButtonStyle.danger
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

        if trade[4] != "pending":
            await interaction.response.send_message(
                "❌ This trade is no longer pending.",
                ephemeral=True
            )
            return

        if interaction.user.id != trade[3]:
            await interaction.response.send_message(
                "❌ You are not the recipient of this trade.",
                ephemeral=True
            )
            return

        update_trade_status(
            self.trade_id,
            "declined"
        )

        await interaction.response.edit_message(
            content=(
                f"❌ Trade **#{self.trade_id}** was declined."
            ),
            view=None
        )