import pygame
import chess

from chessEngine import choose_move


# What this will do is create a dictionary of Chess Images, so that they dont have to be loaded from file all the time
def loadPieceImages(piece_size):
    piece_images = {}
    for color in ["white", "black"]:
        for piece in ["pawn", "knight", "bishop", "rook", "queen", "king"]:
            image_path = f"assets/{color}-{piece}.png"
            piece_image = pygame.image.load(image_path)
            piece_image = pygame.transform.smoothscale(piece_image, (piece_size, piece_size))  
            piece_images[f"{color}-{piece}"] = piece_image
    return piece_images

# Draws the empty board
def drawBoard(screen):
    colors = [pygame.Color(238,238,210), pygame.Color(118, 150, 86)]
    square_size = screen.get_height() // 8 # Temporary 

    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(col * square_size, row * square_size, square_size, square_size))

# Draws the pieces on the board based on the current board state
def draw_pieces(screen, board, chess_images):
    # Iterate through pieces:
    for square, piece in board.piece_map().items():
        piece_name = chess.piece_name(piece.piece_type)
        color = "white" if piece.color == chess.WHITE else "black"
        
        chess_piece_image = chess_images[f"{color}-{piece_name}"]
        x = chess.square_file(square)  
        y = 7 - chess.square_rank(square)

        screen.blit(chess_piece_image, (x * screen.get_height() // 8, y * screen.get_height() // 8)) #

# Adding highlighting
def highlightSquare(screen, selected_square):
    if selected_square is None:
        return
    
    square_size = screen.get_height() // 8
    col = chess.square_file(selected_square)
    row = 7 - chess.square_rank(selected_square)

    highlight = pygame.Surface((square_size, square_size), pygame.SRCALPHA) #The SRCALPHA apparently highlights
    highlight.fill((255, 255, 0, 100)) # Yellow with transparency

    screen.blit(highlight, (col * square_size, row * square_size)) 

# Highlight losing king on checkmate (revise this later) 
def highlight_checkmate(screen, board):
    if not board.is_checkmate():
        return

    king_square = board.king(board.turn)  # Losing king
    square_size = screen.get_height() // 8

    col = chess.square_file(king_square)
    row = 7 - chess.square_rank(king_square)

    highlight = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
    highlight.fill((255, 0, 0, 110))  # Transparent red

    screen.blit(highlight, (col * square_size, row * square_size))

# Choosing to return just a chess_square (e.g. 0-63 not e.g. e4 or b7 etc)
def getClickedSquare(mouse_pos, square_size):
    x, y = mouse_pos
    # Prevents out of bounds
    if 0 <= x < square_size * 8 and 0 <= y < square_size * 8:
        col = x // square_size
        row = y // square_size
        chess_square = chess.square(col, 7 - row)
        return chess_square
    return None

# Draw terminal on the right side
def draw_terminal(screen, logs):
    font = pygame.font.SysFont("consolas", 18)

    pygame.draw.rect(
        screen, 
        pygame.Color("lightgray"),
        pygame.Rect(800, 0, 400, 800) # For now
    )

    for i, message in enumerate(logs[-30:]): 
        text = font.render(message, True, pygame.Color("black"))
        screen.blit(text, (810, 10 + i * 20)) # For now

# Checkmate detection, to have a nice message, but vscode autocompleted the rest lol
def check_game_status(board, logs):
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            logs.append("Checkmate! Black wins.")
        else:
            logs.append("Checkmate! White wins.")
    elif board.is_stalemate():
        logs.append("Stalemate! It's a draw.")
    elif board.is_insufficient_material():
        logs.append("Draw due to insufficient material.")
    elif board.can_claim_threefold_repetition():
        logs.append("Draw by threefold repetition.")
    elif board.can_claim_fifty_moves():
        logs.append("Draw by fifty-move rule.")


# Main function to run the GUI, called from main 
def run_gui(board):
    pygame.init()
    screen = pygame.display.set_mode((1200, 800)) # Sets up the window
    chess_images = loadPieceImages(screen.get_height() // 8) # Creates a dictionary of chess pieces from the files
    clock = pygame.time.Clock() 
    running = True

    # Main loop 
    logs = ["Chess engine initialized", "Waiting for player move...", "\n"]
    selected_square = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if board.turn != chess.WHITE:
                        continue # Dont process clicks if not white's turn 

                    square = getClickedSquare(event.pos, screen.get_height() // 8)
                    if square == None: 
                        continue

                    if selected_square is None: # If no square is selected by user
                        # Make sure it is a piece of the current player and also not empty square
                        piece = board.piece_at(square)
                        if piece is not None and piece.color == board.turn: # This is the check
                            selected_square = square
                    else:
                        # Special case to promote pawns
                        piece = board.piece_at(selected_square)
                        promotion = None
                        if piece.piece_type == chess.PAWN:
                            if chess.square_rank(square) == 7: # Currently this only works for white promotion (engine handles on its own)
                                promotion = chess.QUEEN
                        move = chess.Move(selected_square, square, promotion=promotion)

                        if move in board.legal_moves:
                            move_name = board.san(move)
                            board.push(move)
                            selected_square = None
                            print(move)
                            logs.append(f"White: {move_name}")
                            check_game_status(board, logs)
                        else: 
                            print("Ilegal move")
                        selected_square = None

        # Engine move
        if board.turn == chess.BLACK and not board.is_game_over(claim_draw=True):
            move = choose_move(board)
            possible_moves = list(board.legal_moves)
            move_name = board.san(move)
            logs.append("Possible moves:\n")
            ## The following is logs for random engine 
            logs.append(", ".join(board.san(m) for m in possible_moves))
            logs.append(f"Engine plays: {move_name}")
            logs.append("\n")
            ## End random engine logs
            board.push(move)
            print(f"Engine plays: {move}")
            check_game_status(board, logs)



        ## Render code
        screen.fill("white")
        drawBoard(screen)
        highlightSquare(screen, selected_square)
        highlight_checkmate(screen, board)
        draw_pieces(screen, board, chess_images)
        draw_terminal(screen, logs)
        ## End render code

        pygame.display.flip()
        clock.tick(60) # limits to 60 fps

    pygame.quit()    