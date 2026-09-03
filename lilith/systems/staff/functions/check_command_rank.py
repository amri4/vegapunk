from .get_member_rank import get_member_rank
from .get_command_rank import get_command_rank


def check_command_rank(member, command_name):

    required = get_command_rank(
        member.guild,
        command_name
    )

    # No rank requirement configured
    if required is None:
        return True

    member_rank = get_member_rank(member)

    # User has no staff rank
    if member_rank is None:
        return False

    return (
        member_rank["level"]
        >= required["required_level"]
    )