from .get_ranks import get_ranks


def get_member_rank(member):

    if member is None or member.guild is None:
        return None

    ranks = get_ranks(member.guild)

    member_role_ids = {
        role.id
        for role in member.roles
    }

    member_ranks = [
        rank
        for rank in ranks
        if rank[2] in member_role_ids
    ]

    if not member_ranks:
        return None

    # Level 1 is the highest rank.
    return min(
        member_ranks,
        key=lambda rank: rank[3]
    )