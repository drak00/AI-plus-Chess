"""
	LIGHT and DARK AI BOTS 
	Press 'A' on the keyboard to activate/deactivate AI mode (Light VS Dark)
"""
import random
from math import inf
from engine import Move
light_pieces = {} # dictionary of light pieces on the board (keys = "row,col"; values = chess piece eg "kl")
dark_pieces  = {} # dictionary of dark pieces on the board (keys = "row,col"; values = chess piece eg "kl")

piece_values = {
    "kl":20000, "ql":900, "rl":500, "bl":330, "nl":320, "pl":100, "  ":0,\
    "kd":-20000, "qd":-900, "rd":-500, "bd":-330, "nd":-320, "pd":-100
}

square_values = {
    "pl":[
        [55, 55, 55, 55, 55, 55, 55, 55],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5,  5, 10, 25, 25, 10,  5,  5],
        [0,  0,  0, 20, 20,  0,  0,  0],
        [5, -5,-10,  0,  0,-10, -5,  5],
        [5, 10, 10,-20,-20, 10, 10,  5],
        [0,  0,  0,  0,  0,  0,  0,  0]
    ],
    
    "nl":[
        [-50,-40,-30,-30,-30,-30,-40,-50],
        [-40,-20,  0,  0,  0,  0,-20,-40],
        [-30,  0, 10, 15, 15, 10,  0,-30],
        [-30,  5, 15, 20, 20, 15,  5,-30],
        [-30,  0, 15, 20, 20, 15,  0,-30],
        [-30,  5, 10, 15, 15, 10,  5,-30],
        [-40,-20,  0,  5,  5,  0,-20,-40],
        [-50,-40,-30,-30,-30,-30,-40,-50]
    ],

    "bl":[
        [-20,-10,-10,-10,-10,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5, 10, 10,  5,  0,-10],
        [-10,  5,  5, 10, 10,  5,  5,-10],
        [-10,  0, 10, 10, 10, 10,  0,-10],
        [-10, 10, 10, 10, 10, 10, 10,-10],
        [-10,  5,  0,  0,  0,  0,  5,-10],
        [-20,-10,-10,-10,-10,-10,-10,-20]
    ],

    "rl":[
        [0,  0,  0,  0,  0,  0,  0,  0],
        [5, 10, 10, 10, 10, 10, 10,  5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [0,  0,  0,  5,  5,  0,  0,  0]
    ],

    "ql":[
        [-20,-10,-10, -5, -5,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5,  5,  5,  5,  0,-10],
        [-5,  0,  5,  5,  5,  5,  0, -5],
        [0,  0,  5,  5,  5,  5,  0, -5],
        [-10,  5,  5,  5,  5,  5,  0,-10],
        [-10,  0,  5,  0,  0,  0,  0,-10],
        [-20,-10,-10, -5, -5,-10,-10,-20]
    ],

    # middle game
    "kl":[
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-20,-30,-30,-40,-40,-30,-30,-20],
        [-10,-20,-20,-20,-20,-20,-20,-10],
        [20, 20,  0,  0,  0,  0, 20, 20],
        [20, 30, 10,  0,  0, 10, 30, 20]
    ],

    # end game
    # "kl":[
    #     [-50,-40,-30,-20,-20,-30,-40,-50],
    #     [-30,-20,-10,  0,  0,-10,-20,-30],
    #     [-30,-10, 20, 30, 30, 20,-10,-30],
    #     [-30,-10, 30, 40, 40, 30,-10,-30],
    #     [-30,-10, 30, 40, 40, 30,-10,-30],
    #     [-30,-10, 20, 30, 30, 20,-10,-30],
    #     [-30,-30,  0,  0,  0,  0,-30,-30],
    #     [-50,-30,-30,-30,-30,-30,-30,-50]
    # ]


    "  ":[
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]    
    ],

    #middle game
    "kd":[
        [-20,-30,-10, 0,  0,-10,-30,-20],
        [-20,-20, 0,  0,  0, 0,-20, -20],
        [10, 20, 20, 20, 20, 20, 20, 10],
        [20, 30, 30, 40, 40, 30, 30, 20],
        [30, 40, 40, 50, 50, 40, 40, 30],
        [30, 40, 40, 50, 50, 40, 40, 30],
        [30, 40, 40, 50, 50, 40, 40, 30],
        [30, 40, 40, 50, 50, 40, 40, 30]    
    ],

    "pd":[
        [0,  0,  0,  0,  0,  0,  0,  0],
        [-5,-10,-10, 20, 20,-10,-10,-5],
        [-5, 5, 10,  0,  0, 10,  5,  5],
        [0,  0,  0,-20,-20,  0,  0,  0],
        [-5, -5,-10,-25,-25,-10, -5, -5],
        [-10,-10,-20,-30,-30,-20,-10,-10],
        [-50,-50,-50,-50,-50,-50,-50,-50],
        [-55,-55,-55,-55,-55,-55,-55,-55]    
    ],

    "nd":[
        [50, 40, 30, 30, 30, 30, 40, 50],
        [40, 20,  0, -5, -5,  0, 20, 40],
        [30, -5,-10,-15,-15,-10, -5, 30],
        [30,  0,-15,-20,-20,-15,  0, 30],
        [30, -5,-15,-20,-20,-15, -5, 30],
        [30, -0,-10,-15,-15,-10,  0, 30],
        [40, 20,  0,  0,  0,  0, 20, 40],
        [50, 40, 30, 30, 30, 30, 40, 50]  
    ],
    
    "bd":[
        [20, 10, 10, 10, 10, 10, 10, 20],
        [10, -5,  0,  0,  0,  0, -5, 10],
        [10,-10,-10,-10,-10,-10,-10,10],
        [10,  0,-10,-10,-10,-10,  0, 10],
        [10, -5, -5,-10,-10, -5, -5, 10],
        [10,  0, -5,-10,-10, -5,  0, 10],
        [10,  0,  0,  0,  0,  0,  0, 10],
        [20, 10, 10, 10, 10, 10, 10, 20]   
    ],

    "rd":[
        [0,  0,  0, -5, -5,  0,  0,  0],
        [5,  0,  0,  0,  0,  0,  0,  5],
        [5,  0,  0,  0,  0,  0,  0,  5],
        [5,  0,  0,  0,  0,  0,  0,  5],
        [5,  0,  0,  0,  0,  0,  0,  5],
        [5,  0,  0,  0,  0,  0,  0,  5],
        [-5,-10,-10,-10,-10,-10,-10,-5],
        [0,  0,  0,  0,  0,  0,  0,  0]
    ],

    "qd":[
        [20, 10, 10,  5,  5, 10, 10, 20],
        [10,  0,  5,  0,  0,  0,  0, 10],
        [10,  -5, -5, -5, -5, -5, 0, 10],
        [0,  0, -5, -5,  -5, -5,  0,  5],
        [5,  0, -5, -5, -5, -5,  0,  5],
        [10,  0, -5, -5, -5, -5,  0, 10],
        [10,  0,  0,  0,  0,  0,  0, 10],
        [20, 10, 10,  5,  5, 10, 10, 20]    
    ]

}

def evaluate(board):
    """
        Evaluates chess board

        input parameter(s):
        board --> The chess board to be evaluated

        return parameter(s):
        score --> The board evaluation
    """
    score = 0

    for i in range(len(board)):
        for j in range(len(board[i])):
            # Add piece value and it's current square value (A Queen on d4 will be worth 900 + 5)
            piece_value = piece_values[board[i][j]] + square_values[board[i][j]][i][j]
            # Add piece value to overall board score
            score += piece_value
    
    return score


def minimax(game_state, depth, alpha=-inf, beta=inf):
    """
        Determine best move to play

        input parameter(s):
        game_state --> Game_state object
        depth --> The number of moves ahead to check before deciding best move
        alpha --> alpha value to use for alpha beta pruning. Default is -inf
        beta --> beta value to use for alpha beta pruning. Default is inf

        return parameter(s):
        best_move --> The best move to play
        max_eval --> Evaluation of best_move
    """
    # Breaking condition
    if (depth == 0) or (game_state.check_mate) or (game_state.stale_mate):
        return None, evaluate(game_state.board)
    
    # Get valid moves
    moves = game_state.get_valid_moves()[0]

    if moves: # If there are valid moves
        best_move = random.choice(moves) # Select a random move as best_move
    else: # If there are no valid moves
        return None, evaluate(game_state.board)

    if game_state.light_to_move: # If it is light's turn to play
        max_eval = -inf
        for move in moves:
            game_state.make_move(move, True) # make move in look_ahead mode
            # Call minimax on all possible moves after above move
            current_eval = minimax(game_state, depth-1, alpha, beta)[1]
            game_state.undo_move()

            # Update best_move and current_eval
            if current_eval > max_eval:
                max_eval = current_eval
                best_move = move
            
            # alpha beta pruning
            alpha = max(alpha, current_eval)
            if beta <= alpha:
                break

        return best_move, max_eval
    
    else: # If it is light's turn to play
        min_eval = inf
        for move in moves:
            game_state.make_move(move, True) # make move in look_ahead mode
            # Call minimax on all possible moves after above move
            current_eval = minimax(game_state, depth-1, alpha, beta)[1]
            game_state.undo_move()

            # Update best_move and current_eval
            if current_eval < min_eval:
                min_eval = current_eval
                best_move = move
            
            # alpha beta pruning
            beta = min(beta, current_eval)
            if beta <= alpha:
                break

        return best_move, min_eval


def ai_light_move(gs):
    """
        makes automated valid light moves

        input parameter(s):
        gs --> Game_state object

        return parameter(s):
        light_move --> move made for light team
        gs         --> Game_state object
    """

    ### TODO: edit to your unique algorithm (mini-max w/ pruning, etc) ###
    ###		  Static evaluation of the board can be done with 'light_pieces' and 'dark_pieces' dictionaries ###

	
    move = minimax(gs, 3)[0] # Move as decided by minimax

    # create move copy (only copy (start_row, start_col) & (end_row, end_col) of move object)
    light_move = Move((move.start_row, move.start_col), (move.end_row, move.end_col), gs.board)

    gs.make_move(light_move) # make move

    # handles pawn promotion
    if (light_move.end_row == 0) and (light_move.piece_moved[0] == "p"):\
        gs.board[light_move.end_row][light_move.end_col] = random.choice(("ql", "rl", "bl", "nl")) # randomly select promotion piece

    # update light pieces position dictionary 
    # light_pieces.pop("{},{}".format(light_move.start_row, light_move.start_col))
    # light_pieces["{},{}".format(light_move.end_row, light_move.end_col)] = light_move.piece_moved

    # # remove pieces captured from dark_piece dictionary for faster static board evaluation in your mini-max algorithm rewrite
    # if light_move.piece_captured != "  " and not light_move.en_passant_captured:
    #     dark_pieces.pop("{},{}".format(light_move.end_row, light_move.end_col))
    # elif light_move.en_passant_captured:
    #     dark_pieces.pop("{},{}".format(light_move.end_row+1, light_move.end_col if gs.light_to_move else light_move.end_row-1, light_move.end_col))

    return light_move, gs


def ai_dark_move(gs):
	"""
		makes automated valid dark moves

		input parameter(s):
		gs --> Game_state object

		return parameter(s):
		dark_move --> move made for dark team
		gs        --> Game_state object
	"""
	
	### TODO: edit to your unique algorithm (mini-max w/ pruning, etc) ###
	###		  Static evaluation of the board can be done with 'light_pieces' and 'dark_pieces' dictionaries ###
	valid_moves, turn = gs.get_valid_moves()
	
	if valid_moves:
		move = random.choice(valid_moves) # select random move to make

		# create move copy (only copy (start_row, start_col) & (end_row, end_col) of move object)
		dark_move = Move((move.start_row, move.start_col), (move.end_row, move.end_col), gs.board)

		gs.make_move(dark_move) # make move

		# handles pawn promotion
		if (dark_move.end_row == 7) and (dark_move.piece_moved[0] == "p"):\
			gs.board[dark_move.end_row][dark_move.end_col] = random.choice(("qd", "rd", "bd", "nd")) # randomly select promotion piece

		# update dark pieces position dictionary
		# dark_pieces.pop("{},{}".format(dark_move.start_row, dark_move.start_col))
		# dark_pieces["{},{}".format(dark_move.end_row, dark_move.end_col)] = dark_move.piece_moved

		# # remove pieces captured from light_piece dictionary for faster static board evaluation in your mini-max algorithm rewrite 
		# if dark_move.piece_captured != "  " and not dark_move.en_passant_captured:
		# 	light_pieces.pop("{},{}".format(dark_move.end_row, dark_move.end_col))
		# elif dark_move.en_passant_captured:
		# 	light_pieces.pop("{},{}".format(dark_move.end_row+1, dark_move.end_col if gs.light_to_move else dark_move.end_row-1, dark_move.end_col))
	else:
		dark_move = None

	return dark_move, gs


def ai_move(gs):
	"""
		determines the turn for both team's AI 
		also saves a running memory of the board state with moves and captures

		input parameter(s):
		gs --> Game_state object

		return parameter(s):
		move --> dark or light AI move
		gs   --> Game_state object

	"""

	if not light_pieces:
		for i in range(len(gs.board)):
			for j in range(len(gs.board[i])):
				if gs.board[i][j][1] == "l":
					light_pieces["{},{}".format(i, j)] = gs.board[i][j]

	if not dark_pieces:
		for i in range(len(gs.board)):
			for j in range(len(gs.board[i])):
				if gs.board[i][j][1] == "d":
					dark_pieces["{},{}".format(i, j)] = gs.board[i][j]

	return ai_light_move(gs) if gs.light_to_move else ai_dark_move(gs)


def ai_reset():
	"""
		resets the light pieces and dark pieces dictionaries when AI mode is activated/deactivated (in case moves were made outside AI mode)

		input parameter(s):
		None

		output parameter(s):
		None
	"""
	light_pieces.clear()
	dark_pieces.clear()