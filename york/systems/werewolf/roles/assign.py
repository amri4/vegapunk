import random


def assign_roles(
    db,
    players,
    werewolves,
    seers,
    doctors
):
    if werewolves < 1:
        return None

    if werewolves + seers + doctors > len(players):
        return None

    villagers = (
        len(players)
        - werewolves
        - seers
        - doctors
    )

    roles = (
        ["werewolf"] * werewolves
        + ["seer"] * seers
        + ["doctor"] * doctors
        + ["villager"] * villagers
    )

    random.shuffle(roles)

    for player, role in zip(players, roles):
        db.update(
            "werewolf_players",
            "role = ?",
            "id = ?",
            (role, player[0])
        )

    return True
