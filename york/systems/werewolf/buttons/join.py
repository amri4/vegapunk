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
        message = interaction.message
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
        players = [
        player
        for player in db.fetchall("werewolf_players")
        if player[1] == current_game
        ]
        player_count = len(players)

        embed = discord.Embed(
            title="🐺 Werewolf game lobby",
            description="Click the buttons below to join/leave\n\n Waiting for players..."
        )
        embed.add_field(
            name="👤 Players in lobby",
            value=f"**{player_count}** player(s)",
            inline=True
        )
        await interaction.message.edit(embed=embed)
        await interaction.response.send_message(
            "🐺 You have been added to the game",
            ephemeral=True
        )