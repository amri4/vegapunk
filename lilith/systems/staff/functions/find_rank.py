import unicodedata

from .get_ranks import get_ranks


def normalize(text):
    text = unicodedata.normalize(
        "NFKC",
        text
    )

    return " ".join(
        text.casefold().strip().split()
    )


def find_rank(guild, argument):

    if guild is None or not argument:
        return None

    argument = argument.strip()

    # Role mention
    if argument.startswith("<@&") and argument.endswith(">"):
        argument = argument[3:-1]

    # Role ID
    if argument.isdigit():

        role_id = int(argument)

        for rank in get_ranks(guild):

            if rank[2] == role_id:
                return rank

        return None

    search = normalize(argument)

    ranks = get_ranks(guild)

    # Exact rank-name match
    for rank in ranks:

        if normalize(rank[1]) == search:
            return rank

    # Exact Discord role-name match
    for rank in ranks:

        role = guild.get_role(rank[2])

        if role and normalize(role.name) == search:
            return rank

    return None