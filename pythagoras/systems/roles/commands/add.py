import discord
from discord.ext import commands


@commands.command(
    name="addrole",
    help="Create a new server role."
)
async def addrole(ctx, *, name: str):

    name = name.strip()

    if not name:
        await ctx.send(
            "❌ Please provide a role name."
        )
        return

    role = await ctx.guild.create_role(
        name=name,
        reason=f"Created by {ctx.author}"
    )

    await ctx.send(
        f"✅ Created role {role.mention}."
    )


def setup(bot):
    bot.add_command(addrole)