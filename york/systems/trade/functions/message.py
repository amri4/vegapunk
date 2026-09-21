from .embed import create_trade_embed


async def update_trade_message(
    message,
    trade_id
):
    embed = create_trade_embed(
        trade_id,
        message.guild
    )

    if embed is None:
        return

    await message.edit(
        embed=embed
    )