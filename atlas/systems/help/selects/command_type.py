import discord


class CommandTypeSelect(discord.ui.Select):

    def __init__(self, help_view):

        self.help_view = help_view

        super().__init__(
            placeholder="Choose command type...",
            options=[
                discord.SelectOption(
                    label="Prefix Commands",
                    value="prefix",
                    description="Show prefix commands",
                    emoji="💬"
                ),
                discord.SelectOption(
                    label="Slash Commands",
                    value="slash",
                    description="Show slash commands",
                    emoji="⚡"
                )
            ]
        )

    async def callback(self, interaction):

        view = self.help_view

        if interaction.user.id != view.author.id:
            await interaction.response.send_message(
                "This help menu belongs to someone else.",
                ephemeral=True
            )
            return

        view.mode = self.values[0]
        view.page = 0

        view.refresh()

        await interaction.response.edit_message(
            embed=view.embed(),
            view=view
        )