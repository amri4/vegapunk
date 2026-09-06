import discord


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
        name = f"`/{command.qualified_name}`"
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