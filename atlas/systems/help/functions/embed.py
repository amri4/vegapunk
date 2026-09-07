import discord


async def get_command_mentions(bot):
    commands = await bot.tree.fetch_commands()

    return {
        command.name: command.mention
        for command in commands
    }


async def build_help_embed(
    bot,
    categories,
    category_names,
    page
):
    bot_name = getattr(bot, "bot_name", "Bot")

    embed = discord.Embed(
        title=f"📖 {bot_name} Help",
        description="⚡ **Slash Commands**"
    )

    if not category_names:
        embed.add_field(
            name="No Commands",
            value="No slash commands were found.",
            inline=False
        )
        return embed

    category = category_names[page]
    command_list = categories[category]

    mentions = await get_command_mentions(bot)

    lines = []

    for command in command_list:
        name = mentions.get(
            command.name,
            f"`/{command.name}`"
        )

        description = (
            command.description
            or "No description provided."
        )

        lines.append(
            f"**{name}**\n{description}"
        )

    embed.add_field(
        name=f"📂 {category}",
        value="\n\n".join(lines),
        inline=False
    )

    embed.set_footer(
        text=f"Category {page + 1}/{len(category_names)}"
    )

    return embed