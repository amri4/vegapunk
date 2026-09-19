import discord


class BountyModal(discord.ui.Modal):

    def __init__(self, item):
        super().__init__(
            title="Buy Bounty"
        )

        self.item = item

        self.amount = discord.ui.TextInput(
            label="Berry amount",
            placeholder="How many berries do you want to spend?",
            required=True,
            min_length=1,
            max_length=10
        )

        self.add_item(self.amount)

    async def on_submit(self, interaction):
        try:
            amount = int(self.amount.value)
        except ValueError:
            await interaction.response.send_message(
                "❌ Enter a whole number.",
                ephemeral=True
            )
            return

        if amount <= 0:
            await interaction.response.send_message(
                "❌ The amount must be greater than 0.",
                ephemeral=True
            )
            return

        response = self.item["function"](
            interaction,
            amount
        )

        await interaction.response.send_message(
            response,
            ephemeral=True
        )