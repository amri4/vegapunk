from .get_ranks import get_ranks


async def arrange_roles(guild):

    ranks = get_ranks(guild)

    ranks.sort(
        key=lambda rank: rank[3],
        reverse=True
    )

    bot_member = guild.me

    if bot_member is None:
        return False

    bot_role = bot_member.top_role

    position = bot_role.position - 1

    for rank in ranks:

        role = guild.get_role(
            rank[2]
        )

        if role is None:
            continue

        if role >= bot_role:
            continue

        if position < 1:
            break

        await role.edit(
            position=position
        )

        position -= 1

    return True