from discord import app_commands

from .categories import get_category


def get_prefix_commands(bot):
    categories = {}

    for command in bot.commands:

        if command.name == "help":
            continue

        category = get_category(command.callback)

        categories.setdefault(category, [])
        categories[category].append(command)

    return dict(sorted(categories.items()))


def get_slash_commands(bot):
    categories = {}

    for command in bot.tree.get_commands():

        if isinstance(command, app_commands.Group):
            continue

        if command.name == "help":
            continue

        category = get_category(command.callback)

        categories.setdefault(category, [])
        categories[category].append(command)

    return dict(sorted(categories.items()))