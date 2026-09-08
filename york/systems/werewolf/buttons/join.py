import discord

class JoinButton(discord.ui.Button):
    def __init__(self, gane_id):
        super().__init__(
            label="Join",
            emoji="➕️",
            style=discord.ButtonStyle.success
        )