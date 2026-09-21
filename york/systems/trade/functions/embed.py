import discord

from .trades import get_trade
from .offers import get_offers


def create_trade_embed(
    trade_id,
    guild
):
    trade = get_trade(
        trade_id
    )

    if trade is None:
        return None

    offers = get_offers(
        trade_id
    )

    sender_id = trade[2]
    receiver_id = trade[3]

    sender = guild.get_member(
        sender_id
    )

    receiver = guild.get_member(
        receiver_id
    )

    sender_name = (
        sender.display_name
        if sender
        else f"User {sender_id}"
    )

    receiver_name = (
        receiver.display_name
        if receiver
        else f"User {receiver_id}"
    )

    sender_offers = []
    receiver_offers = []

    for offer in offers:
        user_id = offer[1]
        item_id = offer[2]
        amount = offer[3]

        line = f"• **{item_id}** ×{amount:,}"

        if user_id == sender_id:
            sender_offers.append(line)
        elif user_id == receiver_id:
            receiver_offers.append(line)

    if not sender_offers:
        sender_text = "*Nothing yet*"
    else:
        sender_text = "\n".join(
            sender_offers
        )

    if not receiver_offers:
        receiver_text = "*Nothing yet*"
    else:
        receiver_text = "\n".join(
            receiver_offers
        )

    embed = discord.Embed(
        title=f"🤝 Trade #{trade_id}",
        description=(
            f"### {sender_name}\n"
            f"{sender_text}\n\n"
            f"### {receiver_name}\n"
            f"{receiver_text}"
        )
    )

    return embed