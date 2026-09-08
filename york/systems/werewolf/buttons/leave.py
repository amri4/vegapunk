import discord
import mycord

db = mycord.DB()

class LeaveButton(discord.ui.Button):
    def __init__(self, game_id):
        super().__init__(
            label="Leave",
            emoji="➖️",
            style=discord.ButtonStyle.danger
        )
        self.game_id = game_id
        self.callback = self.join_callback

    async def leave_callback(
        self,
        interaction: discord.Interaction
    ):
        message = interaction.message
        player_exists = db.exists(
            "werewolf_players",
            "game_id = ? AND user_id = ?",
            (self.game_id, interaction.user.id)
        )
        if not player_exists:
            await interaction.response.send_message(
                "You are already not in this game",
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
        if player[1] == self.game_id
        ]
        player_count = len(players)

        player_mentions = "\n".join(
            f"<@{player[2]}>"
            for player in players
        )

        embed = discord.Embed(
            title="🐺 Werewolf game lobby",
            description="Click the buttons below to join/leave\n\n Waiting for players..."
        )
        embed.add_field(
            name="👤 Players in lobby",
            value=f"**{player_count}** player(s)\n{player_mentions}",
            inline=True
        )
        await message.edit(embed=embed)
        
        await interaction.response.send_message(
            "🐺 You have been removed from the game",
            ephemeral=True
        )