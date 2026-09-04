import discord

from ..functions.get_ranks import get_ranks


async def role_update(before, after):

    if before.guild is None:
        return

    # Get all staff ranks for this server
    ranks = get_ranks(before.guild)

    if not ranks:
        return

    staff_role_ids = {
        rank[2]
        for rank in ranks
    }

    # Roles added to the member
    added_roles = [
        role
        for role in after.roles
        if role not in before.roles
    ]

    # Check whether a staff-rank role was added
    added_staff_roles = [
        role
        for role in added_roles
        if role.id in staff_role_ids
    ]

    if not added_staff_roles:
        return

    # The newly added staff role becomes their rank.
    new_staff_role = added_staff_roles[-1]

    # Find any other staff-rank roles they currently have
    other_staff_roles = [
        role
        for role in after.roles
        if (
            role.id in staff_role_ids
            and role.id != new_staff_role.id
        )
    ]

    if not other_staff_roles:
        return

    try:
        await after.remove_roles(
            *other_staff_roles,
            reason="Lilith: member can only have one staff rank."
        )

    except discord.Forbidden:
        print(
            f"[Lilith] Cannot remove extra staff rank roles "
            f"from {after}."
        )

    except discord.HTTPException as error:
        print(
            f"[Lilith] Failed to remove extra staff rank roles "
            f"from {after}: {error}"
        )


def setup(bot):
    bot.add_listener(
        role_update,
        "on_member_update"
    )