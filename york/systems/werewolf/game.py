import mycord

from .roles.assign import assign_roles

db = mycord.DB()


def start_game(game_id):
    game = db.fetchone(
        "werewolf_games",
        "id = ?",
        (game_id,)
    )
    real_players = [
        player
        for player in db.fetchall("werewolf_players")
        if player[1] == game_id and player[3] == 0
    ]

    real_count = len(real_players)

    bots_needed = max(0, 5 - real_count)

    for i in range(bots_needed):
        db.insert(
            "werewolf_players",
            "game_id, is_bot, display_name",
            (game_id, 1, f"York Bot {i + 1}")
        )
    db.update(
        "werewolf_games",
        "status = ?",
        "id = ?",
        ("active", game_id)
    )
    db.update(
        "werewolf_games",
        "phase = ?",
        "id = ?",
        ("night", game_id)
    )
    players = [
        player
        for player in db.fetchall("werewolf_players")
        if player[1] == game_id
    ]

    assign_roles(
        db,
        players,
        werewolves,
        seers,
        doctors
    )
    return True