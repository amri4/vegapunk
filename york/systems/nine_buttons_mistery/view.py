import random

import discord


class MysteryButton(discord.ui.Button):
    def __init__(self, position, reward):
        super().__init__(
            label="📦",
            style=discord.ButtonStyle.secondary,
            row=position // 3
        )

        self.position = position
        self.reward = reward

    async def callback(self, interaction: discord.Interaction):
        view = self.view

        if view.player_id != interaction.user.id:
            await interaction.response.send_message(
                "❌ This isn't your game.",
                ephemeral=True
            )
            return

        if self.disabled:
            return

        self.disabled = True
        view.tries -= 1

        if self.reward is not None:
            self.label = view.reward_emojis[self.reward]
            self.style = discord.ButtonStyle.success
            view.found += 1
        else:
            self.label = "❌"
            self.style = discord.ButtonStyle.danger

        view.update_buttons()

        if view.tries == 0:
            for button in view.children:
                button.disabled = True

            await interaction.response.edit_message(
                embed=view.finished_embed(),
                view=view
            )
            return

        await interaction.response.edit_message(
            embed=view.game_embed(),
            view=view
        )


class MysteryView(discord.ui.View):
    def __init__(self, player_id):
        super().__init__(timeout=120)

        self.player_id = player_id
        self.tries = 3
        self.found = 0

        self.rewards = [
            "berries",
            "ticket",
            "gem"
        ]

        self.reward_emojis = {
            "berries": "💰",
            "ticket": "🎟️",
            "gem": "💎"
        }

        reward_positions = random.sample(range(9), 3)

        for position in range(9):
            reward = None

            if position in reward_positions:
                reward = self.rewards[reward_positions.index(position)]

            self.add_item(
                MysteryButton(position, reward)
            )

    def update_buttons(self):
        for button in self.children:
            if button.disabled:
                continue

    def game_embed(self):
        return discord.Embed(
            title="🎁 Mystery Box",
            description=(
                "There are **3 hidden rewards** among the boxes!\n"
                "Find as many as you can.\n\n"
                f"🎯 **Tries remaining: {self.tries}**"
            )
        )

    def finished_embed(self):
        return discord.Embed(
            title="🎁 Mystery Box — Finished!",
            description=(
                f"You found **{self.found}/3 rewards**! 🎉\n\n"
                "Thanks for playing!"
            )
        )

    async def on_timeout(self):
        for button in self.children:
            button.disabled = True