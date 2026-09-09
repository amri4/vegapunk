import random
import discord
import mycord

from .roles.assign import assign_roles
from .views.night import NightView
from .views.voting import VotingView

db = mycord.DB()

MIN_PLAYERS = 5


def get_game(game_id):
    return db.fetchone(
        "werewolf_games",
        "id = ?",
        (game_id,)
    )


def get_players(game_id):
    return [
        player
        for player in db.fetchall("werewolf_players")
        if player[1] == game_id
    ]


def get_alive_players(game_id):
    return [
        player
        for player in get_players(game_id)
        if player[5] == 1
    ]


def get_player(game_id, player_id):
    return db.fetchone(
        "werewolf_players",
        "id = ? AND game_id = ?",
        (player_id, game_id)
    )


def real_player_count(game_id):
    return len([
        player
        for player in get_players(game_id)
        if player[3] == 0
    ])


def add_york_bots(game_id):
    needed = max(0, MIN_PLAYERS - real_player_count(game_id))

    existing_bots = [
        player
        for player in get_players(game_id)
        if player[3] == 1
    ]

    for index in range(needed):
        db.insert(
            "werewolf_players",
            "game_id, is_bot, display_name",
            (
                game_id,
                1,
                f"York Bot {len(existing_bots) + index + 1}"
            )
        )


def validate_setup(game_id):
    game = get_game(game_id)
    players = get_players(game_id)

    if game is None:
        return False, "The game no longer exists."

    if len(players) < MIN_PLAYERS:
        return False, f"The game needs at least {MIN_PLAYERS} players."

    werewolves = game[6]
    seers = game[7]
    doctors = game[8]

    if werewolves < 1:
        return False, "There must be at least 1 werewolf."

    if werewolves + seers + doctors > len(players):
        return False, "There are more special roles than players."

    if seers < 0 or doctors < 0 or werewolves < 0:
        return False, "Role counts cannot be negative."

    return True, None


def set_phase(game_id, phase, round_number=None):
    if round_number is None:
        db.update(
            "werewolf_games",
            "phase = ?",
            "id = ?",
            (phase, game_id)
        )
    else:
        db.update(
            "werewolf_games",
            "phase = ?, round = ?",
            "id = ?",
            (phase, round_number, game_id)
        )


def player_label(player):
    if player[3] == 1:
        return player[6] or "York Bot"
    return f"<@{player[2]}>"


def lobby_text(game_id):
    players = get_players(game_id)

    if players:
        names = "\n".join(player_label(player) for player in players)
    else:
        names = "Nobody yet."

    return (
        f"**{len(players)} player(s)**\n"
        f"{names}"
    )


async def update_lobby(message, game_id):
    embed = discord.Embed(
        title="🐺 Werewolf game lobby",
        description="Click the buttons below to join or leave."
    )
    embed.add_field(
        name="👤 Players",
        value=lobby_text(game_id),
        inline=False
    )

    await message.edit(
        embed=embed
    )


def store_action(game_id, round_number, phase, player_id, action, target_id):
    db.delete(
        "werewolf_actions",
        "game_id = ? AND round = ? AND phase = ? AND player_id = ?",
        (game_id, round_number, phase, player_id)
    )

    db.insert(
        "werewolf_actions",
        "game_id, round, phase, player_id, action, target_id",
        (
            game_id,
            round_number,
            phase,
            player_id,
            action,
            target_id
        )
    )


def get_actions(game_id, round_number, phase):
    return [
        action
        for action in db.fetchall("werewolf_actions")
        if action[1] == game_id
        and action[2] == round_number
        and action[3] == phase
    ]


def required_night_actions(game_id):
    players = get_alive_players(game_id)

    return [
        player
        for player in players
        if player[4] in ("werewolf", "seer", "doctor")
    ]


def all_night_actions_done(game_id):
    required = required_night_actions(game_id)
    actions = get_actions(
        game_id,
        get_game(game_id)[7],
        "night"
    )

    acted = {action[4] for action in actions}
    return all(player[0] in acted for player in required)


def choose_bot_target(game_id, player):
    alive = get_alive_players(game_id)

    candidates = [
        target
        for target in alive
        if target[0] != player[0]
    ]

    if not candidates:
        return None

    if player[4] == "werewolf":
        candidates = [
            target
            for target in candidates
            if target[4] != "werewolf"
        ] or candidates

    return random.choice(candidates)[0]


def choose_bot_doctor_target(game_id):
    alive = get_alive_players(game_id)
    return random.choice(alive)[0] if alive else None


def run_bot_night_actions(game_id):
    game = get_game(game_id)
    round_number = game[7]

    for player in required_night_actions(game_id):
        if player[3] != 1:
            continue

        if player[4] == "doctor":
            target_id = choose_bot_doctor_target(game_id)
        else:
            target_id = choose_bot_target(game_id, player)

        if target_id is not None:
            store_action(
                game_id,
                round_number,
                "night",
                player[0],
                player[4],
                target_id
            )


def majority_target(actions):
    counts = {}

    for action in actions:
        target_id = action[6]
        if target_id is None:
            continue
        counts[target_id] = counts.get(target_id, 0) + 1

    if not counts:
        return None

    highest = max(counts.values())
    winners = [
        target_id
        for target_id, count in counts.items()
        if count == highest
    ]

    return random.choice(winners)


async def resolve_night(game_id, channel):
    game = get_game(game_id)
    round_number = game[7]
    players = get_players(game_id)

    actions = get_actions(
        game_id,
        round_number,
        "night"
    )

    wolf_actions = [
        action
        for action in actions
        if action[5] == "werewolf"
    ]

    doctor_actions = [
        action
        for action in actions
        if action[5] == "doctor"
    ]

    attacked_id = majority_target(wolf_actions)

    protected_ids = {
        action[6]
        for action in doctor_actions
        if action[6] is not None
    }

    killed_id = None

    if attacked_id is not None and attacked_id not in protected_ids:
        killed_id = attacked_id

        db.update(
            "werewolf_players",
            "alive = ?",
            "id = ?",
            (0, killed_id)
        )

    victim = get_player(game_id, killed_id) if killed_id else None

    if victim:
        result = (
            f"🌙 Night {round_number} is over.\n"
            f"💀 {player_label(victim)} was eliminated during the night."
        )
    else:
        result = (
            f"🌙 Night {round_number} is over.\n"
            f"✨ Nobody was eliminated."
        )

    winner = check_winner(game_id)

    if winner:
        await end_game(game_id, channel, winner)
        return

    set_phase(game_id, "day")

    embed = discord.Embed(
        title=f"☀️ Day {round_number}",
        description=result + "\n\nDiscuss what happened, then vote."
    )

    await channel.send(embed=embed)

    await start_voting(game_id, channel)


async def start_night(game_id, channel):
    game = get_game(game_id)

    if game is None:
        return

    round_number = game[7]

    set_phase(game_id, "night")

    run_bot_night_actions(game_id)

    if all_night_actions_done(game_id):
        await resolve_night(game_id, channel)
        return

    embed = discord.Embed(
        title=f"🌙 Night {round_number}",
        description=(
            "Special-role players, choose your action using the buttons below.\n"
            "Your response is private."
        )
    )

    await channel.send(
        embed=embed,
        view=NightView(game_id)
    )


def check_winner(game_id):
    alive = get_alive_players(game_id)

    wolves = [
        player
        for player in alive
        if player[4] == "werewolf"
    ]

    others = [
        player
        for player in alive
        if player[4] != "werewolf"
    ]

    if not wolves:
        return "villagers"

    if len(wolves) >= len(others):
        return "werewolves"

    return None


def add_vote(game_id, round_number, voter_id, target_id):
    db.delete(
        "werewolf_votes",
        "game_id = ? AND round = ? AND voter_id = ?",
        (game_id, round_number, voter_id)
    )

    db.insert(
        "werewolf_votes",
        "game_id, round, voter_id, target_id",
        (
            game_id,
            round_number,
            voter_id,
            target_id
        )
    )


def get_votes(game_id, round_number):
    return [
        vote
        for vote in db.fetchall("werewolf_votes")
        if vote[1] == game_id
        and vote[2] == round_number
    ]


def all_votes_done(game_id):
    alive = get_alive_players(game_id)
    votes = get_votes(game_id, get_game(game_id)[7])

    voted = {vote[3] for vote in votes}
    return all(player[0] in voted for player in alive)


def run_bot_votes(game_id):
    game = get_game(game_id)
    round_number = game[7]

    alive = get_alive_players(game_id)

    for player in alive:
        if player[3] != 1:
            continue

        candidates = [
            target
            for target in alive
            if target[0] != player[0]
        ]

        if not candidates:
            continue

        if player[4] == "werewolf":
            candidates = [
                target
                for target in candidates
                if target[4] != "werewolf"
            ] or candidates

        target = random.choice(candidates)

        add_vote(
            game_id,
            round_number,
            player[0],
            target[0]
        )


async def resolve_votes(game_id, channel):
    game = get_game(game_id)
    round_number = game[7]

    votes = get_votes(game_id, round_number)

    counts = {}

    for vote in votes:
        counts[vote[4]] = counts.get(vote[4], 0) + 1

    if not counts:
        await start_night(game_id, channel)
        return

    highest = max(counts.values())

    candidates = [
        target_id
        for target_id, count in counts.items()
        if count == highest
    ]

    eliminated_id = random.choice(candidates)

    db.update(
        "werewolf_players",
        "alive = ?",
        "id = ?",
        (0, eliminated_id)
    )

    eliminated = get_player(game_id, eliminated_id)

    winner = check_winner(game_id)

    if winner:
        await end_game(game_id, channel, winner)
        return

    embed = discord.Embed(
        title="🗳️ Vote complete",
        description=(
            f"{player_label(eliminated)} was eliminated.\n"
            f"Their role was **{eliminated[4]}**."
        )
    )

    await channel.send(embed=embed)

    set_phase(game_id, "night", round_number + 1)

    await start_night(game_id, channel)


async def start_voting(game_id, channel):
    run_bot_votes(game_id)

    if all_votes_done(game_id):
        await resolve_votes(game_id, channel)
        return

    embed = discord.Embed(
        title="🗳️ Voting",
        description=(
            "Choose a living player to eliminate.\n"
            "Your vote is private."
        )
    )

    await channel.send(
        embed=embed,
        view=VotingView(game_id)
    )


async def end_game(game_id, channel, winner):
    winner_name = (
        "🐺 Werewolves"
        if winner == "werewolves"
        else "👥 Villagers"
    )

    await channel.send(
        embed=discord.Embed(
            title="🏆 Werewolf game over",
            description=f"**{winner_name} win!**"
        )
    )

    db.delete(
        "werewolf_actions",
        "game_id = ?",
        (game_id,)
    )
    db.delete(
        "werewolf_votes",
        "game_id = ?",
        (game_id,)
    )
    db.delete(
        "werewolf_players",
        "game_id = ?",
        (game_id,)
    )
    db.delete(
        "werewolf_games",
        "id = ?",
        (game_id,)
    )


async def start_game(game_id, bot):
    game = get_game(game_id)

    if game is None:
        return False, "The game no longer exists."

    if game[4] != "lobby":
        return False, "This game has already started."

    add_york_bots(game_id)

    valid, error = validate_setup(game_id)

    if not valid:
        return False, error

    players = get_players(game_id)

    result = assign_roles(
        db,
        players,
        game[6],
        game[7],
        game[8]
    )

    if result is None:
        return False, "The role setup is invalid."

    db.update(
        "werewolf_games",
        "status = ?, phase = ?, round = ?",
        "id = ?",
        ("active", "night", 1, game_id)
    )

    channel = bot.get_channel(game[2])

    if channel is None:
        return False, "The game channel could not be found."

    await channel.send(
        embed=discord.Embed(
            title="🐺 Werewolf has started!",
            description="Roles have been assigned. Night 1 begins."
        )
    )

    await start_night(game_id, channel)

    return True, None
