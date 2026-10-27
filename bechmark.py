import chess
from chessEngine import random_engine, material_evaluation_engine, minimax

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
    #result = play_engine_game(random_engine, material_evaluation_engine)
    #print(f"Game result: {result}")

    #v1 vs v2
    """
    random_engine_wins = 0
    material_engine_wins = 0
    ties = 0
    for i in range(1000):
        result = play_engine_game(random_engine, material_evaluation_engine)
        if result == '1-0':
            random_engine_wins += 1
        elif result == '0-1':
            material_engine_wins += 1
        else:
            ties += 1
        print(f"Game {i+1} result: {result}")
    print(f"Random engine wins: {random_engine_wins}")
    print(f"Material evaluation engine wins: {material_engine_wins}")
    print(f"Ties: {ties}")
    print(f"Percent that Material evaluation won: {material_engine_wins / 1000 * 100}%")
    print(f"Percent that Random engine won: {random_engine_wins / 1000 * 100}%")
    print(f"Percent that tied: {ties / 1000 * 100}%")
    """

    #v2 vs v3 (Minimax depth 3 only position info)
    material_engine_wins = 0
    minimax_engine_wins = 0
    ties = 0
    for i in range(1000):
        result = play_engine_game(material_evaluation_engine, 
                                  lambda board: minimax(board, depth=2))
        if result == '1-0':
            material_engine_wins += 1
        elif result == '0-1':
            minimax_engine_wins += 1
        else:
            ties += 1
        print(f"Game {i+1} result: {result}")
    print(f"Material evaluation engine wins: {material_engine_wins}")
    print(f"Minimax engine wins: {minimax_engine_wins}")
    print(f"Ties: {ties}")
    print(f"Percent that Material evaluation won: {material_engine_wins / 1000 * 100}%")
    print(f"Percent that Minimax engine won: {minimax_engine_wins / 1000 * 100}%")
    print(f"Percent that tied: {ties / 1000 * 100}%")

if __name__ == "__main__":
    main()