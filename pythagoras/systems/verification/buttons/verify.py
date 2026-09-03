import discord

from ...config.functions.get_config import get_config


def create_verify_button():

    button = discord.ui.Button(
        label="Verify",
        emoji="✅",
        style=discord.ButtonStyle.success,
        custom_id="verification_verify"
    )

    async def callback(interaction):

        config = get_config(
            interaction.guild
        )

        member_role_id = config["member_role_id"]

        if not member_role_id:
            await interaction.response.send_message(
                "❌ The member role hasn't been configured.",
                ephemeral=True
            )
            return

        member_role = interaction.guild.get_role(
            member_role_id
        )

        if member_role is None:
            await interaction.response.send_message(
                "❌ The configured member role no longer exists.",
                ephemeral=True
            )
            return

        if member_role in interaction.user.roles:
            await interaction.response.send_message(
                "✅ You're already verified.",
                ephemeral=True
            )
            return

        await interaction.user.add_roles(
            member_role,
            reason="Member verification"
        )

        await interaction.response.send_message(
            "✅ You are now verified!",
            ephemeral=True
        )

    button.callback = callback

    return button