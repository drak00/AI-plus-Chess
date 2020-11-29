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
		self.en_passant = [] 	  # flags possible en-passant moves
		self.castling = [] 		  # flags possible casling moves
		self.move_piece = {"p":self.get_pawn_moves, "r":self.get_rook_moves, \
						"q":self.get_queen_moves, "k":self.get_king_moves, \
						"b":self.get_bishop_moves, "n":self.get_knight_moves}

		self.light_king_location =  (7, 4)
		self.dark_king_location  =  (0, 4)
		self.check_mate = False # king is being attacked (initiated by opposing piece)
		self.stale_mate = False # no valid moves (king cornered; initiated by king)
		self.light_king_side_castle = True # light king side castle available (king and right rook not moved)
		self.light_queen_side_castle = True # light queen side castle available (king and left rook not moved)
		self.dark_king_side_castle = True # dark king side castle available (king and right rook not moved)
		self.dark_queen_side_castle = True # dark queen side castle available (king and left rook not moved)

		


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

		# castling

		# light king side
		if self.light_to_move and self.light_king_side_castle:

			# if path is clear
			if self.board[7][5] == "  " and self.board[7][6] == "  ":

				# if path not under attack
				if (not self.is_square_attacked(7, 5)) and (not self.is_square_attacked(7, 6)):
					moves.append(Move((7, 4), (7, 6), self.board))
					self.castling.append(Move((7, 4), (7, 6), self.board))

		# light queen side	
		if self.light_to_move and self.light_queen_side_castle:

			# if path is clear	
			if self.board[7][1] == "  " and self.board[7][2] == "  " and self.board[7][3] == "  ":

				# if path not under attack
				if (not self.is_square_attacked(7, 1)) and (not self.is_square_attacked(7, 2)) and (not self.is_square_attacked(7, 3)):
					moves.append(Move((7, 4), (7, 2), self.board))
					self.castling.append(Move((7, 4), (7, 2), self.board))

		# dark king side
		if not self.light_to_move and self.dark_king_side_castle:

			# if path is clear
			if self.board[0][5] == "  " and self.board[0][6] == "  ":

				# if path not under attack
				if (not self.is_square_attacked(0, 5)) and (not self.is_square_attacked(0, 6)):
					moves.append(Move((0, 4), (0, 6), self.board))
					self.castling.append(Move((0, 4), (0, 6), self.board))

		# dark queen side
		if not self.light_to_move and self.dark_queen_side_castle:

			# if path is clear
			if self.board[0][1] == "  " and self.board[0][2] == "  " and self.board[0][3] == "  ":

				# if path not under attach
				if (not self.is_square_attacked(0, 1)) and (not self.is_square_attacked(0, 2)) and (not self.is_square_attacked(0, 3)):
					moves.append(Move((0, 4), (0, 2), self.board))
					self.castling.append(Move((0, 4), (0, 2), self.board))



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
					else: # friendly piece
						break
				else: # off board
					break
		

	def get_queen_moves(self, r, c, moves):
		self.get_bishop_moves(r, c, moves)
		self.get_rook_moves(r, c, moves)


	def make_move(self, move, look_ahead_mode = False):
		"""
			moves pieces on the board

			input parameters:
			move     --> move to be made (Move object)
			look_ahead_mode   --> flag to ignore castling or not (during thinking mode)

			return parameter(s):
			None
		"""
		#if self.move_log:
			#print(self.move_log[-1])

		self.board[move.start_row][move.start_col] = "  "
		self.board[move.end_row][move.end_col] = move.piece_moved
		# if self.en_passant and not look_ahead_mode:
		# 	print(self.en_passant)
		# handles en-passant moves
		if not look_ahead_mode and move in self.en_passant:
			if self.light_to_move:
				move.en_passant_captured = self.board[move.end_row+1][move.end_col]
				self.board[move.end_row+1][move.end_col] = "  "
			else:
				move.en_passant_captured = self.board[move.end_row-1][move.end_col]
				self.board[move.end_row-1][move.end_col] = "  "

		self.move_log.append(move) # log move

		# handles castling moves
		if not look_ahead_mode and move in self.castling:

			# determine rook to be castled
			if move.end_col == 2:
				move.castling_rook = self.board[move.start_row][0]
				self.board[move.start_row][0] = "  "
				self.board[move.end_row][3] = "r" + self.board[move.end_row][move.end_col][1] # castle rook
			elif move.end_col == 6:
				move.castling_rook = self.board[move.start_row][7]
				self.board[move.start_row][7] = "  "
				self.board[move.end_row][5] = "r" + self.board[move.end_row][move.end_col][1] # castle rook


		self.light_to_move = not self.light_to_move # next player to move

		if not look_ahead_mode:
			self.castling = [] # reset castling
			self.en_passant = [] # reset en-passant

			# dark en-passant
			if (move.start_row == 6 and move.piece_moved == "pl" and move.start_row - move.end_row == 2):

				# from left of light pawn
				if (move.end_col -1 >= 0 and self.board[move.end_row][move.end_col-1] == "pd"):
					self.en_passant.append(Move((move.end_row, move.end_col-1), (move.end_row+1, move.end_col), self.board))

				# from right of light pawn
				elif (move.end_col +1 <= len(self.board[0])-1 and self.board[move.end_row][move.end_col+1] == "pd"):
					self.en_passant.append(Move((move.end_row, move.start_col+1), (move.end_row+1, move.end_col), self.board))

			# light en-passant
			if (move.start_row == 1 and move.piece_moved == "pd" and move.end_row - move.start_row == 2):

				# from left of dark pawn
				if (move.end_col -1 >= 0 and self.board[move.end_row][move.end_col-1] == "pl"):
					self.en_passant.append(Move((move.end_row, move.start_col-1), (move.end_row-1, move.end_col), self.board))

				# from right of dark pawn
				elif (move.end_col +1 <= len(self.board[0])-1 and self.board[move.end_row][move.end_col+1] == "pl"):
					self.en_passant.append(Move((move.end_row, move.end_col+1), (move.end_row-1, move.end_col), self.board))


		# update king's position
		if move.piece_moved == "kl":
			self.light_king_location = (move.end_row, move.end_col)

			if not look_ahead_mode:	

				# non castling king move
				if not move.castling_rook:
					self.light_king_side_castle = False
					self.light_queen_side_castle = False

				# castling king moves
				# queen side castled
				elif move.castling_rook and move.end_col == 2:
					self.light_queen_side_castle = False

				# king side castled	
				elif move.castling_rook and move.end_col == 6:
					self.light_king_side_castle = False

		elif move.piece_moved == "kd":
			self.dark_king_location = (move.end_row, move.end_col)

			if not look_ahead_mode:	

				# non castling king move
				if not move.castling_rook:
					self.dark_king_side_castle = False
					self.dark_queen_side_castle = False

				# castling king moves
				# queen side castled
				elif move.castling_rook and move.end_col == 2:
					self.dark_queen_side_castle = False

				# king side castled	
				elif move.castling_rook and move.end_col == 6:
					self.dark_king_side_castle = False


		# check rook moves for castling

		if not look_ahead_mode:
			# light rooks
			if move.start_row == 7 and move.start_col == 0:
				self.light_queen_side_castle = False
			elif move.start_row == 7 and move.start_col == 7:
				self.light_king_side_castle = False
			
			# dark rooks
			elif move.start_row == 0 and move.start_col == 0:
				self.dark_queen_side_castle = False
			elif move.start_row == 0 and move.start_col == 7:
				self.dark_king_side_castle = False


	def undo_move(self, look_ahead_mode = False):
		"""
			undoes last move

			input parameter(s):
			look_ahead_mode   -->  flag for thinking mode vs playing mode (false = playing mode)

			return parameter(s):
			None
		"""
		if self.move_log:
			last_move = self.move_log.pop()
			self.board[last_move.start_row][last_move.start_col] = last_move.piece_moved
			self.board[last_move.end_row][last_move.end_col] = last_move.piece_captured
			#print("piece captured ==> {}".format(last_move.piece_captured))

			# handles enpassant
			self.light_to_move = not self.light_to_move
			if last_move.en_passant_captured:
				self.en_passant.append(Move((last_move.start_row, last_move.start_col), (last_move.end_row, last_move.end_col), self.board)) # recall en-passant valid move
				
				if self.light_to_move:
					self.board[last_move.end_row+1][last_move.end_col] = last_move.en_passant_captured
				else:
					self.board[last_move.end_row-1][last_move.end_col] = last_move.en_passant_captured

			# handles checkmate and stalemate
			self.check_mate = False if self.check_mate else False
			self.stale_mate = False if self.stale_mate else False

			# update king's position
			if last_move.piece_moved == "kl":
				self.light_king_location = (last_move.start_row, last_move.start_col)

				# undoing first-time non-castling light king move (for castling)
				if last_move.start_row == 7 and last_move.start_col == 4 and not last_move.castling_rook:

					# ensure no king moves in past moves (first time king move!)
					count = 0
					for past_move in self.move_log:
						if (past_move.piece_moved == last_move.piece_moved) and (past_move.start_row == last_move.start_row) and \
						(past_move.start_col == last_move.start_col):
							count += 1
							break
					if count == 0:
						self.light_queen_side_castle = True
						self.light_king_side_castle = True

			elif last_move.piece_moved == "kd":
				self.dark_king_location = (last_move.start_row, last_move.start_col)

				# undoing first-time non-castling dark king move (for castling)
				if last_move.start_row == 0 and last_move.start_col == 4 and not last_move.castling_rook:

					# ensure no king moves in past moves (first time king move!)
					count = 0
					for past_move in self.move_log:
						if (past_move.piece_moved == last_move.piece_moved) and (past_move.start_row == last_move.start_row) and \
						(past_move.start_col == last_move.start_col):
							count += 1
							break
					if count == 0:
						self.dark_queen_side_castle = True
						self.dark_king_side_castle = True

			# handles castling
			if last_move.castling_rook:
				if last_move.piece_moved == "kl" and last_move.end_col == 2:
					self.light_queen_side_castle = True
					self.board[7][3] = "  "
					self.board[7][0] = "rl"
				elif last_move.piece_moved == "kl" and last_move.end_col == 6:
					self.light_king_side_castle = True
					self.board[7][5] = "  "
					self.board[7][7] = "rl"
				elif last_move.piece_moved == "kd" and last_move.end_col == 2:
					self.dark_queen_side_castle = True
					self.board[0][3] = "  "
					self.board[0][0] = "rd"
				elif last_move.piece_moved == "kd" and last_move.end_col == 6:
					self.dark_king_side_castle = True
					self.board[0][5] = "  "
					self.board[0][7] = "rd"

			# undoing first-time rook moves (for castling)
			# light king side rook 
			if last_move.piece_moved == "rl":
				if last_move.start_row == 7 and last_move.start_col == 7:

					# ensure no rook moves in past moves (first time rook move!)
					count = 0
					for past_move in self.move_log:
						if (past_move.piece_moved == last_move.piece_moved) and (past_move.start_row == last_move.start_row)\
						and (past_move.start_col == last_move.start_col):
							count += 1
							break

					if count == 0:
						self.light_king_side_castle = True

				# light queen side rook
				elif last_move.start_row == 7 and last_move.start_col == 0:

					# ensure no rook moves in past moves (first time rook move!)
					count = 0
					for past_move in self.move_log:
						if (past_move.piece_moved == last_move.piece_moved) and (past_move.start_row == last_move.start_row)\
						and (past_move.start_col == last_move.start_col):
							count += 1
							break

					if count == 0:
						self.light_queen_side_castle = True

			#dark king side rook
			elif last_move.piece_moved == "rd":
				if last_move.start_row == 0 and last_move.start_col == 7:

					# ensure no rook moves in past moves (first time rook move!)
					count = 0
					for past_move in self.move_log:
						if (past_move.piece_moved == last_move.piece_moved) and (past_move.start_row == last_move.start_row)\
						and (past_move.start_col == last_move.start_col):
							count += 1
							break

					if count == 0:
						self.dark_king_side_castle = True

				# dark queen side rook
				elif last_move.start_row == 0 and last_move.start_col == 0:

					# ensure no rook moves in past moves (first time rook move!)
					count = 0
					for past_move in self.move_log:
						if (past_move.piece_moved == last_move.piece_moved) and (past_move.start_row == last_move.start_row)\
						and (past_move.start_col == last_move.start_col):
							count += 1
							break

					if count == 0:
						self.dark_queen_side_castle = True

			# interactive
			if not look_ahead_mode:
				print("undoing ->", last_move.get_chess_notation())
		else:
			print("All undone!")


	def get_valid_moves(self):
		"""
			gives the valid piece moves on the board while considering potential checks

			input parameter(s):
			None

			return parameter(s):
			moves --> list of vlid move objects
			turn  --> char of current player turn ('l' for light, 'd' for dark)
		"""

		moves, turn = self.get_possible_moves()
		for move in moves[::-1]: # reverse iteration
			self.make_move(move, True)
			self.light_to_move = not self.light_to_move
			in_check = self.is_in_check()
			if in_check:
				moves.remove(move)
			self.undo_move(True)
			self.light_to_move = not self.light_to_move

		if in_check and len(moves) == 0:
			self.check_mate = True
		elif not in_check and len(moves) == 0:
			self.stale_mate = True
			
			# handles undoing
		else:
			self.check_mate = False
			self.stale_mate = False

		return moves, turn


	def get_possible_moves(self):
		"""
			gives naive possible moves of pieces on the board without taking checks into 
			account
			
			input parameters:
			None

			return parameter(s):
			moves --> list of possible move objects
			turn  --> char of current player turn ('l' for light, 'd' for dark)
		"""

		moves = []
		#if self.en_passant:
		for obj in self.en_passant:
			moves.append(obj)
		
		turn = "l" if self.light_to_move else "d"

		for i in range(len(self.board)):
			for j in range(len(self.board[i])):
				if self.board[i][j][1] == turn:
					self.move_piece[self.board[i][j][0]](i, j, moves)

		return moves, turn


	def is_in_check(self):
		"""
			determines if current player isnin check (king under attack)

			input parameter(s):
			None

			return parameter(s):
			bool of True or False
		"""
		if self.light_to_move:
			return self.is_square_attacked(self.light_king_location[0], self.light_king_location[1])
		else:
			return self.is_square_attacked(self.dark_king_location[0], self.dark_king_location[1])


	def is_square_attacked(self, r, c):
		"""
			determines if enemy can attack given board position

			input parameter(s):
			r     --> board row (int)
			c     --> board column (int)

			return parameter(s):
			bool of True or False
		"""

		turn = 'l' if self.light_to_move else "d" # allies turn 
		opp_turn = "d" if self.light_to_move else "l" # opponents turn

		# check for all possible knight attacks
		checks = ((1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (2, -1), (-2, -1), (-2, 1))
		for loc in checks:
			end_row = r + loc[0]
			end_col = c + loc[1]

			if 0<= end_row < 8 and 0<= end_col< 8:
				if self.board[end_row][end_col][1] == opp_turn and self.board[end_row][end_col][0] == "n":
					return True


		# check for all possible pawn attacks
		checks = ((-1, -1), (-1, 1)) if self.light_to_move else ((1, -1), (1, 1))
		for loc in checks:
			end_row = r + loc[0]
			end_col = c + loc[1]

			if 0<= end_row < 8 and 0<= end_col < 8:
				if self.board[end_row][end_col][1] == opp_turn and self.board[end_row][end_col][0] == "p":
					return True

		# check for all possible bishop or queen or king attacks
		checks = ((1, -1), (1, 1), (-1, -1), (-1, 1))
		for loc in checks:
			for i in range(1, 8):
				end_row = loc[0]*i + r
				end_col = loc[1]*i + c

				if 0<= end_row < 8 and 0<= end_col < 8:
					if self.board[end_row][end_col][1] == turn:
						break

					elif (i == 1) and (self.board[end_row][end_col][1] == opp_turn) and (self.board[end_row][end_col][0] == "k"):
						break

					elif self.board[end_row][end_col][1] == opp_turn:
						if self.board[end_row][end_col][0] == "b" or self.board[end_row][end_col][0] == "q":
							return True
						else:
							break

		# check for all possible rook or queen or king attacks
		checks = ((1, 0), (-1, 0), (0, 1), (0, -1))
		for loc in checks:
			for i in range(1, 8):
				end_row = loc[0]*i + r
				end_col = loc[1]*i + c

				if 0<= end_row < 8 and 0<= end_col < 8:
					if self.board[end_row][end_col][1] == turn:
						break

					elif (i == 1) and (self.board[end_row][end_col][1] == opp_turn) and (self.board[end_row][end_col][0] == "k"):
						break

					elif (self.board[end_row][end_col][1] == opp_turn):
						if self.board[end_row][end_col][0] == "r" or self.board[end_row][end_col][0] == "q":
							return True
						else:
							break

		return False



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
		self.en_passant_captured = None # piece captured during en-passant
		self.castling_rook = None # rook castled during castling

	def get_chess_notation(self):
		"""
			creates a live commentary of pieces moved on the chess board during a game

			input parameter(s):
			None

			return parameter(s)
			commentary (string)
		"""
		
		if self.en_passant_captured:
			return self.piece_moved[0].upper() + "(" + self.get_rank_file(self.start_row, self.start_col) + ") to " + self.get_rank_file(self.end_row, self.end_col) + \
				"(" + self.en_passant_captured[0].upper() + " captured!)"
		
		elif not self.en_passant_captured and self.piece_captured != "  ":
			return self.piece_moved[0].upper() + "(" + self.get_rank_file(self.start_row, self.start_col) + ") to " + self.get_rank_file(self.end_row, self.end_col) + \
				"(" + self.piece_captured[0].upper() + " captured!)"
		
		elif self.castling_rook:
			return self.piece_moved[0].upper() + "(" + self.get_rank_file(self.start_row, self.start_col) + ") to " + self.get_rank_file(self.end_row, self.end_col) + \
				"(" + "Queen side castling!)" if self.end_col == 2 else "King side castling!)"

		else:
			return self.piece_moved[0].upper() + "(" + self.get_rank_file(self.start_row, self.start_col) + ") to " + \
				self.get_rank_file(self.end_row, self.end_col)


		# return self.piece_moved[0].upper() + "(" + self.get_rank_file(self.start_row, self.start_col) + ") to " + self.get_rank_file(self.end_row, self.end_col) + \
		# 	"(" + self.piece_captured[0].upper() + " captured!)" if self.piece_captured != "  " else self.piece_moved[0].upper() + "(" + self.get_rank_file(self.start_row, self.start_col) + ") to " + \
		# 	self.get_rank_file(self.end_row, self.end_col)


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


