from discord.ext import commands


@commands.command()
async def test(ctx):
    await ctx.send("Atlas systems are working!")

def setup(bot):
    await bot.add_command(test)