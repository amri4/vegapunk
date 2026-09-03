import mycord


db = mycord.PunksDB()


def get_member_rank(member):

    if member is None:
        return None

    rows = db.fetchall("staff_ranks")

    ranks = [
        row
        for row in rows
        if row["guild_id"] == member.guild.id
    ]

    member_role_ids = {
        role.id
        for role in member.roles
    }

    member_ranks = [
        rank
        for rank in ranks
        if rank["role_id"] in member_role_ids
    ]

    if not member_ranks:
        return None

    return max(
        member_ranks,
        key=lambda rank: rank["level"]
    )