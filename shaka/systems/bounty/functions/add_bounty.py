import mycord

from .get_bounty import get_bounty
from .set_bounty import set_bounty


def add_bounty(
    guild_id,
    user_id,
    amount
):
    current_bounty = get_bounty(
        guild_id,
        user_id
    )

    new_bounty = current_bounty + amount

    set_bounty(
        guild_id,
        user_id,
        new_bounty
    )