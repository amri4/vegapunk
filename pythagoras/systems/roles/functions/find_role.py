import discord
import unicodedata


def normalize_role_name(text):
    text = unicodedata.normalize(
        "NFKC",
        text
    )

    return text.casefold().strip()


def find_role(guild, argument):

    if guild is None:
        return None

    if not argument:
        return None

    argument = argument.strip()

    # Role mention
    if argument.startswith("<@&") and argument.endswith(">"):
        argument = argument[3:-1]

    # Role ID
    if argument.isdigit():

        role = guild.get_role(
            int(argument)
        )

        if role:
            return role

    search = normalize_role_name(
        argument
    )

    # Exact match
    for role in guild.roles:

        if normalize_role_name(
            role.name
        ) == search:

            return role

    # Partial match
    matches = [
        role
        for role in guild.roles
        if search in normalize_role_name(
            role.name
        )
    ]

    if len(matches) == 1:
        return matches[0]

    return matches