import chess, random
from chessEngine import random_engine, material_evaluation_engine, minimax, alpha_beta

ENGINES = {
    "material_v1": material_evaluation_engine,
    "minimax_v2": lambda board: minimax(board, depth=2),
    "alpha_beta_v3": lambda board: alpha_beta(board, depth=2),
}

def play_engine_game(white_engine, black_engine):
    board = chess.Board()

    while not board.is_game_over(claim_draw=True):
        if board.turn == chess.WHITE:
            move = white_engine(board)
        else:
            move = black_engine(board)

        board.push(move)

    return board.result(claim_draw=True)

def main():
    # Generalized engine comparison
    engine1 = "minimax_v2"
    engine2 = "alpha_beta_v3"
    engine1_wins = 0
    engine2_wins = 0
    ties = 0
    num_games = 100
    for i in range(num_games):
        # Randomize which engine plays which
        white_engine = ENGINES[engine1]
        black_engine = ENGINES[engine2]
        invert_colors = random.choice([True, False])
        if invert_colors:
            white_engine, black_engine = black_engine, white_engine

        result = play_engine_game(white_engine, black_engine)
        if result == '1-0':
            engine1_wins += int(not invert_colors)
            engine2_wins += int(invert_colors)
        elif result == '0-1':
            engine1_wins += int(invert_colors)
            engine2_wins += int(not invert_colors)
        else:
            ties += 1
        print(f"Game {i+1} result: {result}")
        print(f"{engine1} played {'white' if not invert_colors else 'black'}")
        print(f"{engine2} played {'white' if invert_colors else 'black'}\n")

    print(f"{engine1} wins: {engine1_wins}")
    print(f"{engine2} wins: {engine2_wins}")
    print(f"Ties: {ties}")
    print(f"Percent that {engine1} won: {engine1_wins / num_games * 100}%")
    print(f"Percent that {engine2} won: {engine2_wins / num_games * 100}%")
    print(f"Percent that tied: {ties / num_games * 100}%")

if __name__ == "__main__":
    main()