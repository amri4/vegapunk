import random

def assign_roles(
    db,
    players,
    werewolves,
    seers,
    doctors
):
    if werewolves + seers + doctors > len(players):
        return None
        
    villagers = len(players) - werewolves - seers - doctors
    
    roles = (
        ["werewolf"] * werewolves
        + ["seer"] * seers
        + ["doctor"] * doctors
        + ["villager"] * villagers
    )

    random.shuffle(roles)