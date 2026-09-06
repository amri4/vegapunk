import discord


def build_help_embed(
    bot,
    mode,
    categories,
    category_names,
    page
):

    embed = discord.Embed(
        title="📖 Atlas Help"
    )

    if mode == "prefix":
        embed.description = "💬 **Prefix Commands**"
    else:
        embed.description = "⚡ **Slash Commands**"

    if not category_names:
        embed.add_field(
            name="No commands",
            value="No commands were found.",
            inline=False
        )

        return embed

    category = category_names[page]
    command_list = categories[category]

    lines = []

    for command in command_list:

        if mode == "prefix":

            prefix = bot.command_prefix

            if callable(prefix):
                prefix = ""

            if isinstance(prefix, (list, tuple)):
                prefix = prefix[0] if prefix else ""

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
                f"**`{prefix}{usage}`**\n"
                f"{description}"
            )

        else:

            description = (
                command.description
                or "No description provided."
            )

            if command.id:
                name = (
                    f"</{command.qualified_name}:{command.id}>"
                )
            else:
                name = f"`/{command.qualified_name}`"

            lines.append(
                f"**{name}**\n"
                f"{description}"
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