'''
    Making the chess engine, using python-chess for GUI
    Steps:
    1. Completely random move engine, lol
    1a. Position evaluation (counting material) 
    2. Minmax? 
    3. Train somehow
    4. Read the Alpha go Paper
    5. ??? 

    One thing im realizing, is that this will only be called for generate move. 
    the Chess GUI will feed this program the current board state, this program will then generate a move and return it to the GUI.


    The functions will return a move and a list to append to log in chessGUI.py 
'''

import chess
import random
import time

# This method might not be needed
"""
def play_game(board):
    # Ask the user if they want to play as white or black
    user_color = input("Do you want to play as white or black? (w/b): ")
    if user_color.lower() == 'w':
        user_color = chess.WHITE
    else:
        user_color = chess.BLACK

    while not board.is_game_over(claim_draw=True):
        print(board)
        print()
        if board.turn == user_color:
            move = input("Enter your move in UCI format (e.g., e2e4): ")
            try:
                board.push_uci(move)
            except ValueError:
                print("Invalid move. Please try again.")
        else:
            move = choose_move(board)
            board.push(move)
            print("Thinking...")
            time.sleep(0.5)
            print(f"Engine plays: {move}")
"""

# Right now implementing random move
def choose_move(board):
    #1. Ramdon engine, uncomment to use
    #return random_engine(board) 
    #2. Material evaluation engine, uncomment to use
    #return material_evaluation_engine(board)
    #3. Minimax engine, uncomment to use
    #return minimax(board, 2)
    #return minimax(board, 4)
    #4. Alpha beta pruning engine, uncomment to use
    return alpha_beta(board, 4)
    # return alpha_beta(board, 6)
    

# Evaluate the board position for minimax
# Positive, good for white, negative, good for black
def evaluate_board(board):
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return float('-inf')
        else:
            return float('inf')
    
    # Makes sure it ignores any material advantage if will end in draw
    if board.is_game_over(claim_draw=True):
        return 0
    
    # For now nothing new on if is draw
    return evaluate_material(board)  # Current one 



# chesEngine v0.4
# Alpha beta pruning engine
# wrapper function to return best move
def alpha_beta(board, depth):
    if depth <= 0:
        return None
    best_move = None
    best_eval = float('-inf') if board.turn == chess.WHITE else float('inf')
    legal_moves = list(board.legal_moves)
    player_turn = board.turn
    
    alpha = float('-inf')
    beta = float('inf')
    for m in legal_moves:
        board.push(m)
        eval = alpha_beta_engine(board, depth - 1, alpha, beta, not player_turn)
        board.pop()
        if player_turn == chess.WHITE:
            alpha = max(alpha, eval)
            # Interesting edge case here, if board starts at place where all moves lead to checkmate
            # then best_move would never have been updated 
            if best_move is None or eval > best_eval: 
                best_eval = eval
                best_move = m
        else:
            beta = min(beta, eval)
            if best_move is None or eval < best_eval: # 
                best_eval = eval
                best_move = m
    return best_move 
        
# The actual alpha beta
def alpha_beta_engine(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over(claim_draw=True):
        return evaluate_board(board)
    
    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = alpha_beta_engine(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, max_eval)
            if beta <= alpha:
                break

        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = alpha_beta_engine(board, depth-1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, min_eval)
            if beta <= alpha:
                break
        return min_eval 
    


# chessEngine v0.3
# Minimax engine
#wrapper function for minimax_engine to return the best move 
def minimax(board, depth):
    if depth <= 0: # Just in case 
        return None
    best_move = None
    best_eval = float('-inf') if board.turn == chess.WHITE else float('inf')
    legal_moves = list(board.legal_moves)
    player_turn = board.turn
    cur_best_moves = []
    for m in legal_moves:
        board.push(m)
        eval = minimax_engine(board, depth - 1, not player_turn) 
        board.pop()

        if player_turn == chess.WHITE:
            if eval > best_eval:
                best_eval = eval
                best_move = m
                cur_best_moves = [m]
            elif eval == best_eval:
                cur_best_moves.append(m)
        else:
            if eval < best_eval:
                best_eval = eval
                best_move = m
                cur_best_moves = [m]
            elif eval == best_eval:
                cur_best_moves.append(m)
    return random.choice(cur_best_moves) if cur_best_moves else best_move
    


# Actual minimax engine
def minimax_engine(board, depth, maximizing_player):
    if depth == 0 or board.is_game_over(claim_draw=True):
        return evaluate_board(board)
    
    best_move = None
    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in board.legal_moves:
            board.push(move)
            eval = minimax_engine(board, depth - 1, False)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            board.pop()
            # Implement logic to choose the best move for maximizing player
        return max_eval
    else: 
        minEval = float('inf')
        best_move = None
        for move in board.legal_moves:
            board.push(move)
            eval = minimax_engine(board, depth - 1, True)
            if eval < minEval:
                minEval = eval
                best_move = move
            board.pop()
        return minEval


#This is evaluate material function, given a board, returns sum values of chess pieces
def evaluate_material(board):
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            value = piece_values[piece.piece_type]
            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value
    return score

# chessEngine v0.2
# Chooses moves based on the pieces on the board given a move
def material_evaluation_engine(board):
    legal_moves = list(board.legal_moves)
    cur_best_moves = []
    # Push, evaluate, pop, choose max
    if board.turn == chess.WHITE:
        cur_max = float('-inf')
        cur_max_move = None
        for m in legal_moves:
            board.push(m)
            score = 0
            score = evaluate_material(board)

            if cur_max < score:
                cur_max = score
                cur_max_move = m
                cur_best_moves = []
            if cur_max == score:
                cur_best_moves.append(m)

            board.pop()
    else:    
        cur_min_move = None
        cur_min_move_list = [] # So that it randomizes same point moves
        for m in legal_moves:
            board.push(m)
            score = 0
            score = evaluate_material(board)

            if cur_min > score:
                cur_min = score
                cur_min_move = m
                cur_best_moves = []
            if cur_min == score:
                cur_best_moves.append(m)

            board.pop()
    
    # Here we make sure that if there are multiple moves with the same score, we choose one randomly
    if len(cur_min_move_list) > 0:
        cur_min_move = random.choice(cur_min_move_list)

    return cur_min_move  
    

# chessEngine v0.1
# Ramdonly choose a move 
def random_engine(board):
    legal_moves = list(board.legal_moves)
    move= random.choice(legal_moves)
    return move