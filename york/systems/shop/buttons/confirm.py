import discord

from ..functions.shop import get_item
from ..functions.items import bounty
from ...berries.functions.berries import get_berries, remove_berries


ITEM_FUNCTIONS = {
    "bounty": bounty
}


class ConfirmButton(discord.ui.Button):

    def __init__(
        self,
        item_id,
        user_id
    ):
        super().__init__(
            label="Confirm",
            style=discord.ButtonStyle.success
        )

        self.item_id = item_id
        self.user_id = user_id

    async def callback(
        self,
        interaction: discord.Interaction
    ):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "❌ This isn't your purchase.",
                ephemeral=True
            )
            return

        item = get_item(
            self.item_id
        )

        if item is None:
            await interaction.response.edit_message(
                content="❌ This item no longer exists.",
                embed=None,
                view=None
            )
            return

        title = item[1]
        price = item[3]
        item_type = item[6]

        item_function = ITEM_FUNCTIONS.get(
            item_type
        )

        if item_function is None:
            await interaction.response.edit_message(
                content="❌ This item is not available right now.",
                embed=None,
                view=None
            )
            return

        berries = get_berries(
            interaction.guild.id,
            interaction.user.id
        )

        if berries < price:
            await interaction.response.edit_message(
                content=(
                    f"❌ You need **{price:,} 🍓** to buy "
                    f"**{title}**.\n"
                    f"You only have **{berries:,} 🍓**."
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

        response = item_function(
            interaction,
            price
        )

        await interaction.response.edit_message(
            content=response,
            embed=None,
            view=None
        )