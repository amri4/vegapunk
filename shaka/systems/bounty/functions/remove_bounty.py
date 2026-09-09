from .get_bounty import get_bounty
from .set_bounty import set_bounty


def remove_bounty(
    guild_id,
    user_id,
    amount
):
    current_bounty = get_bounty(
        guild_id,
        user_id
    )

    new_bounty = max(
        0,
        current_bounty - amount
    )

    set_bounty(
        guild_id,
        user_id,
        new_bounty
    )