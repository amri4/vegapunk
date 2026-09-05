import mycord


db = mycord.DB()


def get_ranks(guild):

    rows = db.fetchall(
        "staff_ranks"
    )

    return [
        row
        for row in rows
        if row[0] == guild.id
    ]