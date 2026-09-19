from shaka.systems.bounty.functions.add_bounty import add_bounty

from ..berries.functions.berries import (
    get_berries,
    remove_berries
)


def bounty(interaction, amount):
    guild_id = interaction.guild.id
    user_id = interaction.user.id

    berries = get_berries(
        guild_id,
        user_id
    )

    if berries < amount:
        return (
            f"❌ You only have **{berries:,} <:berries:1550458400800776344>** "
            f"but you're trying to spend **{amount:,} <:berries:1550458400800776344>**."
        )

    remove_berries(
        guild_id,
        user_id,
        amount
    )

    bounty_amount = amount * 10

    add_bounty(
        guild_id,
        user_id,
        bounty_amount
    )

    return (
        f"🏴‍☠️ You received **{bounty_amount:,} bounty** "
        f"for **{amount:,} <:berries:1550458400800776344>**!"
    )