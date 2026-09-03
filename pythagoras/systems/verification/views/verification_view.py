import discord

from ..buttons.verify import create_verify_button


def create_verification_view():

    view = discord.ui.View(
        timeout=None
    )

    view.add_item(
        create_verify_button()
    )

    return view