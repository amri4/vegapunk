from ...berries.functions.berries import add_berries


WIN_REWARD = 500
DRAW_REWARD = 150
LOSS_REWARD = 50


def reward_winner(guild_id, winner_id, loser_id):
    add_berries(guild_id, winner_id, WIN_REWARD)
    add_berries(guild_id, loser_id, LOSS_REWARD)


def reward_draw(guild_id, player_x, player_o):
    add_berries(guild_id, player_x, DRAW_REWARD)
    add_berries(guild_id, player_o, DRAW_REWARD)