from shaka.systems.bounty.functions.bounty import add_bounty

def bounty(interaction, amount):
    bounty_amount = amount * 10

    add_bounty(
        interaction.guild.id,
        interaction.user.id,
        bounty_amount
    )

    return (
        f"🏴‍☠️ You received **{bounty_amount:,} bounty** "
        f"for **{amount:,} <:berries:1550458400800776344>**!"
    )