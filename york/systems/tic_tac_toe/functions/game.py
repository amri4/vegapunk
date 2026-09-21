WINNING_COMBINATIONS = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6)
)


def create_board():
    return [""] * 9


def make_move(board, position, symbol):
    if board[position] != "":
        return False

    board[position] = symbol
    return True


def check_winner(board):
    for a, b, c in WINNING_COMBINATIONS:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]

    return None


def is_draw(board):
    return all(board)


def game_over(board):
    if check_winner(board) is not None:
        return True

    return is_draw(board)