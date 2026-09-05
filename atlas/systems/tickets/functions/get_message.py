async def get_message(ctx):
    return await ctx.bot.wait_for(
        "message",
        check=lambda m: (
            m.author == ctx.author
            and m.channel == ctx.channel
        )
    )