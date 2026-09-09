import discord
import mycord

from ..game import start_game, get_game

db = mycord.DB()


class StartButton(discord.ui.Button):
    def __init__(self, game_id):
        super().__init__(
            label="Start",
            emoji="▶️",
            style=discord.ButtonStyle.primary
        )
        self.game_id = game_id
        self.callback = self.start_callback

    async def start_callback(self, interaction: discord.Interaction):
        game = get_game(self.game_id)

        if game is None:
            await interaction.response.send_message(
                "❌ This game no longer exists.",
                ephemeral=True
            )
            return

        if interaction.user.id != game[3]:
            await interaction.response.send_message(
                "❌ Only the game creator can start the game.",
                ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)

        started, error = await start_game(
            self.game_id,
            interaction.client
        )

        if not started:
            await interaction.followup.send(
                f"❌ {error}",
                ephemeral=True
            )
            return

        self.disabled = True

        try:
            await interaction.message.edit(view=self.view)
        except discord.HTTPException:
            pass

        await interaction.followup.send(
            "🐺 The game has started!",
            ephemeral=True
        )
