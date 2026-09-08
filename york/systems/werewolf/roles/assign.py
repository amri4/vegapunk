import random

def assign_roles(
    players,
    werewolves,
    seers,
    doctors
):
    roles = (
        ["werewolf"] * werewolves
        + ["seer"] * seers
        + ["doctor"] * doctors
        + ["villager"] * villagers
    )

    random.shuffle(roles)
    pass