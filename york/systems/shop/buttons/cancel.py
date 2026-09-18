import discord


class CancelButton(discord.ui.Button):

    def __init__(self, user_id):
        super().__init__(
            label="Cancel",
            style=discord.ButtonStyle.danger
        )

        self.user_id = user_id

    async def callback(self, interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "❌ This isn't your purchase.",
                ephemeral=True
            )
            return

        await interaction.response.edit_message(
            content="❌ Purchase cancelled.",
            embed=None,
            view=None
        )