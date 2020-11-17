## This is the main chess game engine that implements the rules of the game
## and stores the state of the the chess board, including its pieces and moves
import  tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox as mbox

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
		self.light_kings_location = (7, 4)
		self.dark_kings_location = (0, 4)
		self.is_check_mate = False
		self.is_stalemate = False
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

		if self.light_to_move: # light pawns
			if r-1 >= 0 and self.board[r-1][c] == "  ": # one square advance
				moves.append(Move((r, c), (r-1, c), self.board))

				if r == 6 and self.board[r-2][c] == "  ": # two square advance
					moves.append(Move((r, c), (r-2, c), self.board))

			if c-1 >= 0: # left captures
				if r-1 >=0 and self.board[r-1][c-1][1] == "d": # dark piece present
					moves.append(Move((r, c), (r-1, c-1), self.board))

			if c+1 <= len(self.board[0]) - 1: # right captures
				if r-1>= 0  and self.board[r-1][c+1][1] == "d":
					moves.append(Move((r, c), (r-1, c+1), self.board))

		else: # dark pawns

			if r+1 <= 7 and self.board[r+1][c] == "  ": # one square advance
				moves.append(Move((r, c), (r+1, c), self.board))

				if r == 1 and self.board[r+2][c] == "  ": # two square advance
					moves.append(Move((r, c), (r+2, c), self.board))

			if c-1 >= 0: # left captures
				if r+1 <= 7 and self.board[r+1][c-1][1] == "l": # light piece present
					moves.append(Move((r, c), (r+1, c-1), self.board))

			if c+1 <= len(self.board[0]) - 1: # right captures
				if r+1 <= 7 and self.board[r+1][c+1][1] == "l":
					moves.append(Move((r, c), (r+1, c+1), self.board))
					

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
		directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
		enemy_color = "d" if self.light_to_move else "l"

		for d in directions:
			for i in range(1, 8):
				end_row = r + d[0] * i
				end_col = c + d[1] * i

				if 0 <= end_row < 8 and 0 <= end_col < 8:
					destination = self.board[end_row][end_col]
					if destination == "  ":
						moves.append(Move((r, c), (end_row, end_col), self.board))
					elif destination[1] == enemy_color:
						moves.append(Move((r, c), (end_row, end_col), self.board))
						break
					else: # friendly piece
						break
				else: # off board
					break
		


	def get_knight_moves(self, r, c, moves):
		directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
		enemy_color = "d" if self.light_to_move else "l"

		for d in directions:
			end_row = r + d[0]
			end_col = c + d[1]

			if 0 <= end_row < 8 and 0 <= end_col < 8:
				destination = self.board[end_row][end_col]
				if destination[1] == enemy_color or destination == "  ":
					moves.append(Move((r, c), (end_row, end_col), self.board))


	def get_king_moves(self, r, c, moves):
		directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
		enemy_color = "d" if self.light_to_move else "l"

		for d in directions:
			end_row = r + d[0]
			end_col = c + d[1]

			if 0 <= end_row < 8 and 0<= end_col < 8:
				destination = self.board[end_row][end_col]
				if destination[1] == enemy_color or destination == "  ":
					moves.append(Move((r, c), (end_row, end_col), self.board))


	def get_rook_moves(self, r, c, moves):

		directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
		enemy_color = "d" if self.light_to_move else "l"
		
		for d in directions:
			for i in range(1, 8):
				end_row = r + d[0] * i
				end_col = c + d[1] * i

				if 0 <= end_row < 8 and 0 <= end_col <8: # on board
					destination = self.board[end_row][end_col]
					if destination == "  ": # empty
						moves.append(Move((r, c), (end_row, end_col), self.board))
					elif destination[1] == enemy_color:
						moves.append(Move((r, c), (end_row, end_col), self.board))
						break
					else: # freindly piece
						break
				else: # off board
					break
		

	def get_queen_moves(self, r, c, moves):
		self.get_bishop_moves(r, c, moves)
		self.get_rook_moves(r, c, moves)


	def make_move(self, move):
		"""
			moves pieces on the board
		"""
		self.board[move.start_row][move.start_col] = "  "
		self.board[move.end_row][move.end_col] = move.piece_moved
		self.move_log.append(move) # log move
		self.light_to_move = not self.light_to_move # next player to move
		if move.piece_moved == "kl":
			self.light_kings_location = (move.end_row, move.end_col)
		elif move.piece_moved == "kd":
			self.dark_kings_location = (move.end_row, move.end_col)
		#pawnpromotion
		if move.pawnpromotion:
			#window to allow the user enter his choice
			master = tk.Tk()
			master.withdraw()
			while True:
				userDb = simpledialog.askstring("pawns promotion chooser",
												"Enter q to promote to Queen,r to Rook ,b to Bishop or n to Knight: ")
				if userDb is None:
					mbox.showerror("CAN NOT CANCEL","THIS OPERATION CANNOT BE CANCELED")
				elif userDb.lower() not in ["q","n","r","b"]:
					mbox.showerror("WRONG CHOICE", "ENTER ONLY q,r,n or b")
				else:
					self.board[move.end_row][move.end_col] = userDb + move.piece_moved[1]
					master.destroy()
					break


	def undo_move(self, n, look_ahead_mode = False, undo=True):
		"""
			undoes last move
		"""
		if self.move_log:
			last_move = self.move_log.pop()
			self.board[last_move.start_row][last_move.start_col] = last_move.piece_moved
			self.board[last_move.end_row][last_move.end_col] = last_move.piece_captured
			self.light_to_move = not self.light_to_move
			#update light kings and dark kings location after undoing a move
			if self.board[last_move.start_row][last_move.start_col] == "kl" :
				self.light_kings_location = (last_move.start_row, last_move.start_col)
			elif self.board[last_move.start_row][last_move.start_col] == "kd" :
				self.dark_kings_location = (last_move.start_row, last_move.start_col)
			if n:
				print("undoing ->", last_move.get_chess_notation())
				
		else:
			print("All undone!")


	def get_valid_moves(self,move):
		moves = self.get_possible_moves()[0] #generate all moves
		for i in range(len(moves)-1, -1, -1): #for each move, make the move
			self.make_move(moves[i])
			self.light_to_move = not self.light_to_move #change the current player
			if self.king_in_check(): #check to see if move leaves king in check
				moves.remove(moves[i]) #if yes, remove move
			self.light_to_move = not self.light_to_move
			n = False # undo moves should not print undoing
			self.undo_move(n)
		if len(moves) == 0 and self.king_in_check():  # checking if there are no possible valid moves  and king incheck
			self.is_check_mate = True  # check mate
		elif len(moves) == 0:  # checking if there are no possible moves but king not incheck
			self.is_stalemate = True  # stalemate
		else:
			self.is_check_mate = False
			self.is_stalemate = False

		return moves
	def king_in_check(self):
		"""
		A function that check to see if move leaves a king under check or not
		input: None
		:return: True or False
		"""
		if self.light_to_move:
			if self.square_in_check(self.light_kings_location[0], self.light_kings_location[1]):
				return True
			else: return False
		else:
			if self.square_in_check(self.dark_kings_location[0], self.dark_kings_location[1]):
				return True
			else: return False
	def square_in_check(self, r, c):
		"""
		A function that check to see if king is in check
		:param r: a variable representing row
		:param c: a variable representing column
		:return: True or False
		"""
		self.light_to_move = not self.light_to_move #change the current player
		opponents_moves = self.get_possible_moves()[0] #generate all opponenets moves
		self.light_to_move = not self.light_to_move
		for mov in opponents_moves:
			if mov.end_row == r and mov.end_col == c:
				return True
		return False
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
		#pawn promotion
		self.pawnpromotion = (self.piece_moved == "pl" and self.end_row == 0) or (
					self.piece_moved == "pd" and self.end_row == 7)
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
