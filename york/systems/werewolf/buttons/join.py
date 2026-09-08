import discord
import mycord

db = mycord.DB()

class JoinButton(discord.ui.Button):
    def __init__(self, game_id):
        super().__init__(
            label="Join",
            emoji="➕️",
            style=discord.ButtonStyle.success
        )
        self.game_id = game_id
        self.callback = self.join_callback

    async def join_callback(
        self,
        interaction: discord.Interaction
    ):
        player_exists = db.exists(
            "werewolf_players",
            "game_id = ? AND user_id = ?",
            (self.game_id, interaction.user.id)
        )
        if player_exists:
            await interaction.response.send_message(
                "You are already in this game",
                ephemeral=True
            )
            return
        db.insert(
            "werewolf_players",
            "game_id, user_id",
            (self.game_id, interaction.user.id)
        )
        await interaction.response.send_message(
            "🐺 You have been added to the game"
        )