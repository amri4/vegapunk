from .functions.items import bounty


SHOP_ITEMS = [
    {
        "id": "bounty",
        "title": "Bounty",
        "description": "Exchange berries for bounty.",
        "variable": True,
        "function": bounty
    }
]