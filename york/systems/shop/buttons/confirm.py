import discord

from ...berries.functions.berries import (
    get_berries,
    remove_berries
)


class ConfirmButton(discord.ui.Button):

    def __init__(self, item, user_id):
        super().__init__(
            label="Confirm",
            style=discord.ButtonStyle.success
        )

        self.item = item
        self.user_id = user_id

    async def callback(self, interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "❌ This isn't your purchase.",
                ephemeral=True
            )
            return

        price = self.item["price"]

        berries = get_berries(
            interaction.guild.id,
            interaction.user.id
        )

        if berries < price:
            await interaction.response.edit_message(
                content=(
                    f"❌ You need **{price:,} <:berries:1550458400800776344>** to buy "
                    f"**{self.item['title']}**.\n"
                    f"You only have **{berries:,} <:berries:1550458400800776344>**."
                ),
                embed=None,
                view=None
            )
            return

        if not remove_berries(
            interaction.guild.id,
            interaction.user.id,
            price
        ):
            await interaction.response.edit_message(
                content="❌ You don't have enough berries.",
                embed=None,
                view=None
            )
            return

        response = self.item["function"](
            interaction,
            price
        )

        await interaction.response.edit_message(
            content=response,
            embed=None,
            view=None
        )