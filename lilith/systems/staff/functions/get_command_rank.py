import mycord

from .get_ranks import get_ranks


db = mycord.PunksDB()


def get_command_rank(guild, command_name):

    if guild is None:
        return None

    rows = db.fetchall(
        "command_ranks"
    )

    command_name = command_name.casefold()

    command_rank = next(
        (
            row
            for row in rows
            if (
                row[0] == guild.id
                and row[1].casefold() == command_name
            )
        ),
        None
    )

    if command_rank is None:
        return None

    required_level = command_rank[2]

    ranks = get_ranks(
        guild
    )

    rank = next(
        (
            rank
            for rank in ranks
            if rank[3] == required_level
        ),
        None
    )

    return rank