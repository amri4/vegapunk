import discord
import mycord

from ..game import (
    get_game,
    get_player,
    get_alive_players,
    store_action,
    all_night_actions_done,
    resolve_night
)

db = mycord.DB()


class NightActionButton(discord.ui.Button):
    def __init__(self, game_id, actor_id, target_id, label):
        super().__init__(
            label=label,
            style=discord.ButtonStyle.secondary
        )
        self.game_id = game_id
        self.actor_id = actor_id
        self.target_id = target_id
        self.callback = self.action_callback

    async def action_callback(self, interaction: discord.Interaction):
        game = get_game(self.game_id)

        if game is None or game[4] != "active" or game[5] != "night":
            await interaction.response.send_message(
                "❌ This night is no longer active.",
                ephemeral=True
            )
            return

        player = db.fetchone(
            "werewolf_players",
            "game_id = ? AND user_id = ?",
            (
                self.game_id,
                interaction.user.id
            )
        )

        if player is None or player[0] != self.actor_id:
            await interaction.response.send_message(
                "❌ This action is not for you.",
                ephemeral=True
            )
            return

        target = get_player(
            self.game_id,
            self.target_id
        )

        if target is None or target[5] != 1:
            await interaction.response.send_message(
                "❌ That player is no longer alive.",
                ephemeral=True
            )
            return

        if player[4] == "werewolf" and target[4] == "werewolf":
            await interaction.response.send_message(
                "❌ Werewolves cannot target another werewolf.",
                ephemeral=True
            )
            return

        store_action(
            self.game_id,
            game[7],
            "night",
            player[0],
            player[4],
            target[0]
        )

        await interaction.response.send_message(
            f"✅ Your target is {target[6] or f'<@{target[2]}>'}.",
            ephemeral=True
        )

        if all_night_actions_done(self.game_id):
            channel = interaction.client.get_channel(game[2])

            if channel is not None:
                await resolve_night(
                    self.game_id,
                    channel
                )
