from discord.ext import commands

from ..views.help_view import HelpView


@commands.command(
    name="help",
    description="Show Atlas commands."
)
async def help_command(ctx):

    view = HelpView(
        ctx.bot,
        ctx.author
    )

    await ctx.send(
        embed=view.embed(),
        view=view
    )


async def setup(bot):
    bot.add_command(help_command)