"""
	LIGHT and DARK AI BOTS
	Press 'A' on the keyboard to activate/deactivate AI mode (Light VS Dark)
"""
import random
from engine import Move
light_pieces = {} # dictionary of light pieces on the board (keys = "row,col"; values = chess piece eg "kl")
dark_pieces  = {} # dictionary of dark pieces on the board (keys = "row,col"; values = chess piece eg "kl")



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

	valid_moves, turn = gs.get_valid_moves()
	if valid_moves:
		move = random.choice(valid_moves) # select random move to make

		# create move copy (only copy (start_row, start_col) & (end_row, end_col) of move object)
		light_move = Move((move.start_row, move.start_col), (move.end_row, move.end_col), gs.board)

		gs.make_move(light_move) # make move

		# handles pawn promotion
		if (light_move.end_row == 0) and (light_move.piece_moved[0] == "p"):\
			gs.board[light_move.end_row][light_move.end_col] = random.choice(("ql", "rl", "bl", "nl")) # randomly select promotion piece

		# update light pieces position dictionary
		light_pieces.pop("{},{}".format(light_move.start_row, light_move.start_col))
		light_pieces["{},{}".format(light_move.end_row, light_move.end_col)] = light_move.piece_moved

		# remove pieces captured from dark_piece dictionary for faster static board evaluation in your mini-max algorithm rewrite
		if light_move.piece_captured != "  " and not light_move.en_passant_captured:
			dark_pieces.pop("{},{}".format(light_move.end_row, light_move.end_col))
		elif light_move.en_passant_captured:
			dark_pieces.pop("{},{}".format(light_move.end_row+1, light_move.end_col if gs.light_to_move else light_move.end_row-1, light_move.end_col))
	else:
		light_move = None

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
		dark_pieces.pop("{},{}".format(dark_move.start_row, dark_move.start_col))
		dark_pieces["{},{}".format(dark_move.end_row, dark_move.end_col)] = dark_move.piece_moved

		# remove pieces captured from light_piece dictionary for faster static board evaluation in your mini-max algorithm rewrite
		if dark_move.piece_captured != "  " and not dark_move.en_passant_captured:
			light_pieces.pop("{},{}".format(dark_move.end_row, dark_move.end_col))
		elif dark_move.en_passant_captured:
			light_pieces.pop("{},{}".format(dark_move.end_row+1, dark_move.end_col if gs.light_to_move else dark_move.end_row-1, dark_move.end_col))
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
