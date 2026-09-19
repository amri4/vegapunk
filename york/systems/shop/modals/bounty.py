import discord

from ..functions.items import bounty


class BountyModal(discord.ui.Modal, title="Buy Bounty"):

    amount = discord.ui.TextInput(
        label="Berry amount",
        placeholder="Enter how many berries you want to spend",
        required=True,
        min_length=1,
        max_length=10
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            amount = int(self.amount.value)
        except ValueError:
            await interaction.response.send_message(
                "❌ Please enter a whole number.",
                ephemeral=True
            )
            return

        if amount <= 0:
            await interaction.response.send_message(
                "❌ The amount must be greater than 0.",
                ephemeral=True
            )
            return

        response = bounty(
            interaction,
            amount
        )

        await interaction.response.send_message(
            response,
            ephemeral=True
        )