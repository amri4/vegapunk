import discord


async def get_command_mentions(bot):
    commands = await bot.tree.fetch_commands()

    return {
        command.qualified_name: command.mention
        for command in commands
    }


async def build_help_embed(
    bot,
    categories,
    category_names,
    page,
    mode
):
    bot_name = getattr(bot, "bot_name", "Bot")

    if mode == "prefix":
        description = "💬 **Prefix Commands**"
    else:
        description = "⚡ **Slash Commands**"

    embed = discord.Embed(
        title=f"📖 {bot_name} Help",
        description=description
    )

    if not category_names:
        command_type = (
            "prefix" if mode == "prefix"
            else "slash"
        )

        embed.add_field(
            name="No Commands",
            value=f"No {command_type} commands were found.",
            inline=False
        )

        return embed

    category = category_names[page]
    command_list = categories[category]

    lines = []

    if mode == "slash":
        mentions = await get_command_mentions(bot)

        for command in command_list:
            name = mentions.get(
                command.qualified_name,
                f"`/{command.qualified_name}`"
            )

            description = (
                command.description
                or "No description provided."
            )

            lines.append(
                f"**{name}**\n{description}"
            )

    else:
        prefix = bot.command_prefix

        if callable(prefix):
            prefix = ""

        if isinstance(prefix, (list, tuple)):
            prefix = prefix[0] if prefix else ""

        for command in command_list:
            if command.usage:
                usage = command.usage

                if not usage.startswith(command.name):
                    usage = f"{command.name} {usage}"
            else:
                usage = command.name

            description = (
                command.description
                or "No description provided."
            )

            lines.append(
                f"**`{prefix}{usage}`**\n{description}"
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