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
        real_players = [
            player
            for player in db.fetchall("werewolf_players")
            if player[1] == self.game_id and player[3] == 0
        ]

        real_count = len(real_players)

        bots_needed = max(0, 5 - real_count)

        print("Real players:", real_count)
        print("York bots needed:", bots_needed)