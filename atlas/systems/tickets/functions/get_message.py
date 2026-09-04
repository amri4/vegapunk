async def get_message(ctx):
    message = await ctx.bot.wait_for(
        "message",
        check=lambda m: m.author == ctx.author and m.channel == ctx.channel
    )

    return message.content