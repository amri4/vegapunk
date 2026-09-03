import discord


def find_category(guild, name):

    if guild is None:
        return None, "This command can only be used in a server."

    if not name:
        return None, "You need to provide a category name."

    for category in guild.categories:

        if category.name.lower() == name.lower():
            return category, None

    return None, f"❌ Category **{name}** was not found."