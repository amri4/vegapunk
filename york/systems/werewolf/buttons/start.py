import discord
import mycord

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
        
        real_players = [
            player
            for player in db.fetchall("werewolf_players")
            if player[1] == self.game_id and player[3] == 0
        ]

        real_count = len(real_players)

        bots_needed = max(0, 5 - real_count)

        for i in range(bots_needed):
            db.insert(
                "werewolf_players",
                "game_id, is_bot, display_name",
                (self.game_id, 1, f"York Bot {i + 1}")
            )

        print("Real players:", real_count)
        print("York bots needed:", bots_needed)
        self.disabled = True
        await interaction.message.edit(view=self.view)