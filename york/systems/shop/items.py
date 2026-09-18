from .ids import SHOP_CHANNEL_ID
from .functions.items import bounty


SHOP_ITEMS = [
    {
        "id": "bounty",
        "channel_id": SHOP_CHANNEL_ID,
        "title": "Bounty",
        "description": "Exchange berries for bounty.",
        "price": 100,
        "function": bounty
    }
]