from .functions.trades import get_trades

from .views.respond import TradeRespondView
from .views.trade import TradeView


def setup(bot):
    trades = get_trades()

    for trade in trades:

        trade_id = trade[0]
        status = trade[4]

        if status == "pending":

            bot.add_view(
                TradeRespondView(
                    trade_id
                )
            )

        elif status == "accepted":

            bot.add_view(
                TradeView(
                    trade_id
                )
            )