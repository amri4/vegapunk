import discord
import mycord

from ..game import (
    get_game,
    get_alive_players,
    add_vote,
    all_votes_done,
    resolve_votes
)

db = mycord.DB()


class VoteButton(discord.ui.Button):
    def __init__(self, game_id, voter_id, target_id, label):
        super().__init__(
            label=label,
            style=discord.ButtonStyle.secondary
        )
        self.game_id = game_id
        self.voter_id = voter_id
        self.target_id = target_id
        self.callback = self.vote_callback

    async def vote_callback(self, interaction: discord.Interaction):
        game = get_game(self.game_id)

        if game is None or game[4] != "active" or game[5] != "day":
            await interaction.response.send_message(
                "❌ Voting is not active.",
                ephemeral=True
            )
            return

        voter = db.fetchone(
            "werewolf_players",
            "game_id = ? AND user_id = ?",
            (
                self.game_id,
                interaction.user.id
            )
        )

        if voter is None or voter[0] != self.voter_id:
            await interaction.response.send_message(
                "❌ This vote is not for you.",
                ephemeral=True
            )
            return

        if voter[5] != 1:
            await interaction.response.send_message(
                "❌ Dead players cannot vote.",
                ephemeral=True
            )
            return

        alive = get_alive_players(self.game_id)

        if not any(player[0] == self.target_id for player in alive):
            await interaction.response.send_message(
                "❌ That player is no longer alive.",
                ephemeral=True
            )
            return

        add_vote(
            self.game_id,
            game[7],
            voter[0],
            self.target_id
        )

        await interaction.response.send_message(
            "🗳️ Your vote has been recorded.",
            ephemeral=True
        )

        if all_votes_done(self.game_id):
            channel = interaction.client.get_channel(game[2])

            if channel is not None:
                await resolve_votes(
                    self.game_id,
                    channel
                )
