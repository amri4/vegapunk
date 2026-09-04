async def get_message(bot, ctx):
    message = await bot.wait_for(
        "message",
        check=lambda m: m.author == ctx.author and m.channel == ctx.channel
    )

    return message.content