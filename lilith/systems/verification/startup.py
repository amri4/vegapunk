from .buttons.verifybutton import VerificationView


def setup(bot):
    bot.add_view(
        VerificationView()
    )