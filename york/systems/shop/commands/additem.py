import discord
from discord import app_commands

from ..functions.shop import add_item, update_message_id
from ..views.shop import ShopView


@app_commands.command(
    name="additem",
    description="Add an item to the shop."
)
@app_commands.describe(
    title="The item's title.",
    description="The item's description.",
    price="The item's price in berries.",
    channel="The channel where the item will be posted."
)
@app_commands.default_permissions(
    manage_guild=True
)
async def additem(
    interaction: discord.Interaction,
    title: str,
    description: str,
    price: int,
    channel: discord.TextChannel
):
    if price <= 0:
        await interaction.response.send_message(
            "❌ The price must be greater than 0.",
            ephemeral=True
        )
        return

    if not interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message(
            "❌ You don't have permission to add shop items.",
            ephemeral=True
        )
        return

    await interaction.response.defer(
        ephemeral=True
    )

    item_id = add_item(
        title,
        description,
        price,
        channel.id
    )

    embed = discord.Embed(
        title=title,
        description=(
            f"{description}\n\n"
            f"**Price:** {price:,} <:berries:1550458400800776344>"
        )
    )

    message = await channel.send(
        embed=embed,
        view=ShopView(item_id)
    )

    update_message_id(
        item_id,
        message.id
    )

    await interaction.followup.send(
        f"✅ Added **{title}** to {channel.mention}.",
        ephemeral=True
    )


def setup(bot):
    bot.tree.add_command(additem)