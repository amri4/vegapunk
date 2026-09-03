import mycord


db = mycord.PunksDB()


async def arrange_roles(guild):

    rows = db.fetchall("staff_ranks")

    ranks = [
        row
        for row in rows
        if row["guild_id"] == guild.id
    ]

    if not ranks:
        return

    # Highest level first
    ranks.sort(
        key=lambda row: row["level"],
        reverse=True
    )

    bot_member = guild.me

    if bot_member is None:
        return

    bot_role = bot_member.top_role

    # Put the highest staff rank directly
    # below Lilith's highest role.
    position = bot_role.position - 1

    for rank in ranks:

        role = guild.get_role(
            rank["role_id"]
        )

        if role is None:
            continue

        if role >= bot_role:
            continue

        await role.edit(
            position=position,
            reason="Arranging staff hierarchy"
        )

        position -= 1