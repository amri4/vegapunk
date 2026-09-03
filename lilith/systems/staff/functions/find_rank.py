import mycord


db = mycord.PunksDB()


def find_rank(guild, argument):

    if guild is None:
        return None

    if not argument:
        return None

    argument = str(argument).strip()

    # Remove role mention
    if argument.startswith("<@&") and argument.endswith(">"):
        argument = argument[3:-1]

    rows = db.fetchall("staff_ranks")

    ranks = [
        row
        for row in rows
        if row["guild_id"] == guild.id
    ]

    # Role ID
    if argument.isdigit():

        role_id = int(argument)

        for rank in ranks:
            if rank["role_id"] == role_id:
                return rank

        # Level
        level = int(argument)

        for rank in ranks:
            if rank["level"] == level:
                return rank

    # Rank name
    search = argument.casefold()

    for rank in ranks:
        if rank["name"].casefold() == search:
            return rank

    return None