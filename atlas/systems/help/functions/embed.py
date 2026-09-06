import discord


def get_command_mention(bot, command):
    for synced_command in bot.tree.get_commands():
        if synced_command.qualified_name == command.qualified_name:
            return f"</{synced_command.qualified_name}:{synced_command.id}>"

    return f"`/{command.qualified_name}`"


def build_help_embed(bot, categories, category_names, page):
    embed = discord.Embed(
        title="📖 Atlas Help",
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

    lines = []

    for command in command_list:
        name = get_command_mention(bot, command)
        description = command.description or "No description provided."

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