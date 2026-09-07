import random
from dataclasses import dataclass


@dataclass
class WerewolfPlayer:
    user_id: int | None
    name: str
    is_bot: bool = False
    role: str | None = None
    alive: bool = True


class WerewolfGame:

    def __init__(
        self,
        guild,
        channel,
        players,
        role_counts=None
    ):
        self.guild = guild
        self.channel = channel
        self.players = []

        for member in players:
            self.players.append(
                WerewolfPlayer(
                    user_id=member.id,
                    name=member.display_name
                )
            )

        while len(self.players) < 3:
            self.players.append(
                WerewolfPlayer(
                    user_id=None,
                    name=f"York-{len(self.players) + 1}",
                    is_bot=True
                )
            )

        self.role_counts = role_counts or {}

        self.status = "lobby"
        self.phase = None

    async def start(self):
        self.status = "playing"

        self.assign_roles()

        self.phase = "night"

        await self.channel.send(
            "🌙 **Night has fallen...**\n"
            "The Werewolf game is beginning."
        )

    def assign_roles(self):
        roles = []

        werewolves = self.role_counts.get("werewolf")
        seers = self.role_counts.get("seer")
        doctors = self.role_counts.get("doctor")
        villagers = self.role_counts.get("villager")

        if werewolves is None:
            werewolves = max(1, len(self.players) // 3)

        if seers is None:
            seers = 1 if len(self.players) >= 4 else 0

        if doctors is None:
            doctors = 1 if len(self.players) >= 5 else 0

        if villagers is None:
            villagers = (
                len(self.players)
                - werewolves
                - seers
                - doctors
            )

        roles.extend(["werewolf"] * werewolves)
        roles.extend(["seer"] * seers)
        roles.extend(["doctor"] * doctors)
        roles.extend(["villager"] * villagers)

        random.shuffle(roles)

        for player, role in zip(self.players, roles):
            player.role = role

    def get_alive_players(self):
        return [
            player
            for player in self.players
            if player.alive
        ]

    def get_werewolves(self):
        return [
            player
            for player in self.players
            if player.role == "werewolf" and player.alive
        ]

    def get_non_werewolves(self):
        return [
            player
            for player in self.players
            if player.role != "werewolf" and player.alive
        ]

    def check_winner(self):
        werewolves = len(self.get_werewolves())
        others = len(self.get_non_werewolves())

        if werewolves == 0:
            return "villagers"

        if werewolves >= others:
            return "werewolves"

        return None