RARITY_WEIGHTS = {
    "Common": 50,
    "Uncommon": 25,
    "Rare": 15,
    "Epic": 7,
    "Legendary": 3
}


def get_rarity_weight(rarity):
    return RARITY_WEIGHTS.get(
        rarity,
        0
    )