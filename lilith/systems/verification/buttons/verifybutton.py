import discord

from ..setup import db


class VerifyButton(
    discord.ui.Button
):

    def __init__(self):
        super().__init__(
            label="Verify",
            emoji="✅",
            style=discord.ButtonStyle.success,
            custom_id="lilith:verify"
        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):
        config = db.fetchone(
            "verification_config",
            "guild_id = ?",
            (interaction.guild.id,)
        )

        if config is None or config[1] is None:
            await interaction.response.send_message(
                "Tch. Verification hasn't been configured yet."
            )
            return

        if config[3] != 1:
            await interaction.response.send_message(
                "🔓 Verification is currently disabled."
            )
            return

        role = interaction.guild.get_role(
            config[1]
        )

        if role is None:
            await interaction.response.send_message(
                "The configured verification role no longer exists."
            )
            return

        if role in interaction.user.roles:
            await interaction.response.send_message(
                "You're already verified."
            )
            return

        try:
            await interaction.user.add_roles(
                role,
                reason="Lilith verification"
            )

            await interaction.response.send_message(
                "✅ Verification complete. Welcome to the server."
            )

        except discord.Forbidden:
            await interaction.response.send_message(
                "Tch. I can't give you the verification role."
            )

        except discord.HTTPException:
            await interaction.response.send_message(
                "Something went wrong while verifying you. Try again."
            )


class VerificationView(
    discord.ui.View
):

    def __init__(self):
        super().__init__(
            timeout=None
        )

        self.add_item(
            VerifyButton()
        )