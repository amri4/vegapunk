import discord
import mycord

from ..game import start_game

db = mycord.DB()


class StartButton(discord.ui.Button):
    def __init__(self, game_id):
        super().__init__(
            label="Start",
            emoji="▶️",
            style=discord.ButtonStyle.success
        )

        self.game_id = game_id
        self.callback = self.start_callback

    async def start_callback(
        self,
        interaction: discord.Interaction
    ):
        game = db.fetchone(
            "werewolf_games",
            "id = ?",
            (self.game_id,)
        )
        if interaction.user.id != game[3]:
            await interaction.response.send_message(
                "❌ Only the game creator can start the game.",
                ephemeral=True
            )
            return

        if real_count < 1:
            await interaction.response.send_message(
                "❌ There are no players in the game.",
                ephemeral=True
            )
            return
        
        started = start_game(self.game_id)

        print("Real players:", real_count)
        print("York bots needed:", bots_needed)
        self.disabled = True
        await interaction.message.edit(view=self.view)