import discord


class PreviousButton(discord.ui.Button):

    def __init__(self, help_view):

        self.help_view = help_view

        super().__init__(
            emoji="◀️",
            style=discord.ButtonStyle.secondary
        )

    async def callback(self, interaction):

        view = self.help_view

        if interaction.user.id != view.author.id:
            await interaction.response.send_message(
                "This help menu belongs to someone else.",
                ephemeral=True
            )
            return

        if not view.category_names:
            await interaction.response.defer()
            return

        view.page -= 1

        if view.page < 0:
            view.page = len(view.category_names) - 1

        await interaction.response.edit_message(
            embed=view.embed(),
            view=view
        )


class NextButton(discord.ui.Button):

    def __init__(self, help_view):

        self.help_view = help_view

        super().__init__(
            emoji="▶️",
            style=discord.ButtonStyle.secondary
        )

    async def callback(self, interaction):

        view = self.help_view

        if interaction.user.id != view.author.id:
            await interaction.response.send_message(
                "This help menu belongs to someone else.",
                ephemeral=True
            )
            return

        if not view.category_names:
            await interaction.response.defer()
            return

        view.page += 1

        if view.page >= len(view.category_names):
            view.page = 0

        await interaction.response.edit_message(
            embed=view.embed(),
            view=view
        )