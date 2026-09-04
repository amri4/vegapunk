from .get_member_rank import get_member_rank
from .get_command_rank import get_command_rank


def check_command_rank(member, command_name):

    required_rank = get_command_rank(
        member.guild,
        command_name
    )

    # No rank requirement
    if required_rank is None:
        return True

    member_rank = get_member_rank(
        member
    )

    # Member has no staff rank
    if member_rank is None:
        return False

    # Level 1 is the highest rank
    return (
        member_rank[3]
        <= required_rank[3]
    )