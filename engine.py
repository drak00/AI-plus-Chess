## This is the main chess game engine that implements the rules of the game
## and stores the state of the the chess board, including its pieces and moves


class Game_state():
	
	def __init__(self):
		"""
			The chess board is an 8 X 8 dimensional array (Matrix of 8 rows and 8 columns )
			i.e a list of lists. Each element of the Matrix is a string of two characters 
			representing the chess pieces in the order "type" + "colour"

			light pawn = pl
			dark pawn  = pd

			light knight = nl
			dark knight  = nd
			e.t.c

			empty board square = "  " ---> double empty space

		"""

		self.board = [

			["rd", "nd", "bd", "qd", "kd", "bd", "nd", "rd"],
			["pd", "pd", "pd", "pd", "pd", "pd", "pd", "pd"],
			["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
			["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
			["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
			["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
			["pl", "pl", "pl", "pl", "pl", "pl", "pl", "pl"],
			["rl", "nl", "bl", "ql", "kl", "bl", "nl", "rl"]]

		self.light_to_move = True # True = light's turn to play; False = dark's turn to play
		self.move_log = []        # keeps a log of all moves made withing a game
		self.move_piece = {"p":self.get_pawn_moves, "r":self.get_rook_moves, \
						"q":self.get_queen_moves, "k":self.get_king_moves, \
						"b":self.get_bishop_moves, "n":self.get_knight_moves}


	def get_pawn_moves(self, r, c, moves):
		"""
			Calculates all possible pawn moves for a given color (light or dark)
			and appends them to a list

			input parameter(s):
			r     --> starting row (int)
			c     --> starting colum (int)
			moves --> possible moves container (list)

			return parameter(s):
			None
		"""

		## FIX
		if self.light_to_move: # if it's light's turn to move
			
			for i in range(len(self.board)):
				for j in range(len(self.board[i])):
					#first pawn move: move one or two hops if next two rows on same column are empty
					if (i == r-2) and (j == c) and  (r == 6) and (self.board[i][j] == "  "):
						moves.append(Move((r, c), (i, j), self.board)) # create a move object and append to list
					#subsequent pawn moves: one hop foward if square on foward row on same column is empty
					if (i == r-1) and (j == c) and (self.board[i][j] == "  "):
						moves.append(Move((r, c), (i, j), (self.board)))
					#Move to capture opponent pawn: move to next row on column to the left or column to the right to capture opponent
					if (i == r-1) and ((j == c+1) or (j == c-1)) and (self.board[i][j][1] == "d"):
						moves.append(Move((r, c), (i, j), (self.board)))

		

		##FIX
		else: # if it's dark's turn to move

			for i in range(len(self.board)):
				for j in range(len(self.board[i])):
					#first pawn move: move one or two hops if next two rows on same column are empty
					if (i == r+2) and (j == c) and  (r == 1) and (self.board[i][j] == "  "):
						moves.append(Move((r, c), (i, j), self.board)) # create a move object and append to list
					#subsequent pawn moves: one hop foward if square on foward row on same column is empty
					if (i == r+1) and (j == c) and (self.board[i][j] == "  "):
						moves.append(Move((r, c), (i, j), (self.board)))
					#Move to capture opponent pawn: move to next row on column to the left or column to the right to capture opponent
					if (i == r+1) and ((j == c+1) or (j == c-1)) and (self.board[i][j][1] == "l"):
						moves.append(Move((r, c), (i, j), (self.board)))


	def get_bishop_moves(self, r, c, moves):

 		"""
			calculates all possible bishop moves for a given colour (light or dark)
			and appends them to a list

			input parameters:
			r     --> starting row (int)
			c     --> starting column (int)
			moves --> posiible moves container (list)

			return parameter(s):
			None
 		"""

 		##TODO
 		pass


	def get_knight_moves(self, r, c, moves):
 		##TODO
	    pass


	def get_king_moves(self, r, c, moves):
		"""
			calculates all possible king moves for a given colour (light or dark)
			and appends them to a list

			input parameters:
			r     --> starting row (int)
			c     --> starting column (int)
			moves --> posiible moves container (list)

			return parameter(s):
			None
 		"""
 		##TODO
		rows = (r-1, r, r+1)
		columns = (c-1, c, c+1)
		if self.light_to_move: # if it's light's turn to move
			available_squares = (" ", "d") #if square is empty or has a dark piece
			for i in range(len(self.board)):
				for j in range(len(self.board[i])):
					#if square in any direction is empty or has an opponent, move to square or move to capture
					if (i in rows) and (j in columns) and (self.board[i][j][1] in available_squares):
						moves.append(Move((r, c), (i, j), self.board)) # create a move object and append to list 
		
		else: #dark turn to move
			available_squares = (" ", "l")  #if square is empty or has a light piece
			for i in range(len(self.board)):
				for j in range(len(self.board[i])):
					#if square in any direction is empty or has an opponent, move to square or move to capture
					if (i in rows) and (j in columns) and (self.board[i][j][1] in available_squares):
						moves.append(Move((r, c), (i, j), self.board)) # create a move object and append to list 
    


	def get_rook_moves(self, r, c, moves):
 		##TODO
 		pass


	def get_queen_moves(self, r, c, moves):
		##TODO
		pass


	def make_move(self, move):
		"""
			moves pieces on the board
		"""
		self.board[move.start_row][move.start_col] = "  "
		self.board[move.end_row][move.end_col] = move.piece_moved
		self.move_log.append(move) # log move
		self.light_to_move = not self.light_to_move # next player to move


	def undo_move(self, look_ahead_mode = False):
		"""
			undoes last move
		"""
		if self.move_log:
			last_move = self.move_log.pop()
			self.board[last_move.start_row][last_move.start_col] = last_move.piece_moved
			self.board[last_move.end_row][last_move.end_col] = last_move.piece_captured
			self.light_to_move = not self.light_to_move

			print("undoing ->", last_move.get_chess_notation())
		else:
			print("All undone!")


	def get_valid_moves(self):
		return self.get_possible_moves()


	def get_possible_moves(self):

		moves = []

		turn = "l" if self.light_to_move else "d"

		for i in range(len(self.board)):
			for j in range(len(self.board[i])):
				if self.board[i][j][1] == turn:
					self.move_piece[self.board[i][j][0]](i, j, moves)

		return moves, turn



class Move():

	# map ranks to rows
	ranks_to_rows = {"1":7, "2":6, "3":5, "4":4,
					"5":3, "6":2, "7":1, "8":0}

	# map rows to ranks (revers of ranks to rows)
	rows_to_ranks = {row:rank for rank, row in ranks_to_rows.items()}

	# map files to columns 
	files_to_cols = {"a":0, "b":1, "c":2, "d":3,
					"e":4, "f":5, "g":6, "h":7}

	# map columns to files (revers of files to columns)
	cols_to_files = {col:file for file, col in files_to_cols.items()} 

	def __init__(self, start_sq, end_sq, board):
		"""
			A Move class abstracting all parameters needed
			for moving chess pieces on the board

			input parameter(s):
			start_sq --> (row, column) of piece to be moved (tuple)
			end_square --> (row, column) of move destination on the board (tuple)
			board --> board object referencing current state of the board (class Game_state) 
		"""
		self.start_row = start_sq[0] # row location of piece to be moved
		self.start_col = start_sq[1] # column location of piece to be moved
		self.end_row = end_sq[0] # intended row destination of piece to be moved 
		self.end_col = end_sq[1] # intended column destiantion of piece to e moved
		self.piece_moved = board[self.start_row][self.start_col] # actual piece moved
		self.piece_captured = board[self.end_row][self.end_col] # opponent piece if any on the destination square

	def get_chess_notation(self):
		"""
			creates a live commentary of pieces moved on the chess board during a game

			input parameter(s):
			None

			return parameter(s)
			commentary (string)
		"""
		return self.piece_moved[0].upper() + "(" + self.get_rank_file(self.start_row, self.start_col) + ") to " + self.get_rank_file(self.end_row, self.end_col) + \
			"(" + self.piece_captured[0].upper() + " captured!)" if self.piece_captured != "  " else self.piece_moved[0].upper() + "(" + self.get_rank_file(self.start_row, self.start_col) + ") to " + \
			self.get_rank_file(self.end_row, self.end_col)


	def get_rank_file(self, r, c):
		"""
			calls cols_to_file and rows_to_rank attributes

			input parameter(s):
			r --> row to be converted to rank (int)
			c --> column to be converted to file (int)

			return parameter(s):
			"file" + "rank" (str)
		"""
		return self.cols_to_files[c] + self.rows_to_ranks[r]


	def __eq__(self, other):
		"""
			operator overloading for equating two move objects
		"""

		if isinstance(other, Move): # if first (self) and second (other) parameters are both Move objects
			return self.start_row == other.start_row and self.start_col == other.start_col and \
					self.end_row == other.end_row and self.end_col == other.end_col
		else:
			return False


	def __ne__(self, other):
		"""
			"not equals to" --> conventional counterpart to __eq__
		"""
		return self.__eq__(other)


	def __str__(self):
		"""
			operator overloading for printing Move objects
		"""
		return "({}, {}) ({}, {})".format(self.start_row, self.start_col, self.end_row, self.end_col)


