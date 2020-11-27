##This is the GUI displaying all aspects of the chess game and 
##handling user inputs

import pygame as pg
from engine import Game_state, Move
from tkinter import messagebox as mbox
from random import randrange
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox as mbox
from random import randrange as rand
pg.init()

BORDER = 128 # for the ranks and files
WIDTH = HEIGHT = 512 # of the chess board 
DIMENSION = 8 # rows and columns 
OFFSET = 5 # for image scaling
SQ_SIZE = HEIGHT // DIMENSION # size of each board square
MAX_FPS = 15
IMAGES = {}
COLORS = [pg.Color("burlywood1"), pg.Color("darkorange4")]
SOUND = [pg.mixer.Sound("audio/move.wav"), pg.mixer.Sound("audio/capture.wav")]


def load_images():
	"""
		loads images from directory into dictionary with parameters SQ_SIZE and OFFSET 
	"""

	pieces = ["bd", "bl", "kd", "kl", "nd", "nl", "pd", "pl", "qd", "ql", "rd", "rl"]

	for piece in pieces:
		IMAGES[piece] = pg.transform.scale(pg.image.load("images/"+ piece + ".png"), (SQ_SIZE - OFFSET, SQ_SIZE - OFFSET))


def main():
	screen = pg.display.set_mode((WIDTH + BORDER, HEIGHT + BORDER))
	clock = pg.time.Clock()
	#screen.fill(pg.Color("ghostwhite"))
	screen.fill(pg.Color("brown4"))


	gs = Game_state()
	load_images()
	running = True

	square_selected = () # x, y coordinate of selected square 
	player_clicks = [] # list of appended square_selected
	valid_moves = [] 
	while running:

		valid_moves = gs.get_valid_moves(Move)		
		first_click_turn = "l" if gs.light_to_move else "d"
		if first_click_turn == "d":
			if gs.is_check_mate:
				master = tk.Tk()
				master.withdraw()
				mbox.showinfo("WINNER", "LIGHT TEAM WINS")
				master.destroy()
			elif gs.is_stalemate:
				master = tk.Tk()
				master.withdraw()
				mbox.showinfo("NO WINNER", "GAME IS DRAWN")
				master.destroy()
			else:
				# i = randrange(len(valid_moves))
				# move = valid_moves[i]
				# gs.make_move(move)
				# animate(move, screen, gs.board, clock)
				# if move.pawnpromotion:
				# 	s = ["q","n","r","b"]
				# 	x = s[randrange(len(s))]
				# 	gs.board[move.end_row][move.end_col] = x + move.piece_moved[1]

				# best_move = valid_moves[0]
				# for move in valid_moves:
				# 	gs.make_move(move)
				# 	score = evaluation_function(gs.board)
				# 	if score > best_score:
				# 		best_score = score
				# 		best_move = move
				# 	gs.undo_move(look_ahead_mode=True)
				alpha = -2000000
				beta = -2000000
				best_move = None
				depth = 3
				score, best_move = alphabeta(gs.board, best_move, depth, alpha, beta)
				gs.make_move(best_move)
				animate(move, screen, gs.board, clock)
				if move.pawnpromotion:
					gs.board[move.end_row][move.end_col] = "q" + move.piece_moved[1]
				#first_click_turn = "l"
		for e in pg.event.get():
			if e.type == pg.QUIT:
				running = False

			elif e.type == pg.KEYDOWN:
				if e.key == pg.K_u: # u key pressed (undo last move)
					n = True
					gs.undo_move(n)

				elif e.key == pg.K_r: # r key pressed (reset game)
					gs = Game_state()
					valid_moves, turn = [], None
					square_selected = ()
					player_clicks = []
					print("Board reset!")

			elif e.type == pg.MOUSEBUTTONDOWN:
				if first_click_turn == "l":
					location = pg.mouse.get_pos() # x, y location of mouse click
					location_col_transform = location[0] // SQ_SIZE - 1
					location_row_transform = location[1] // SQ_SIZE - 1
					col = (location_col_transform) if (0 <= location_col_transform < 8) else -1
					row = (location_row_transform) if (0 <= location_row_transform < 8) else -1

					if col >= 0 and row >= 0:

						if square_selected == (row, col): # clicked same position twice
							square_selected = ()
							player_clicks = []

						else: # new position clicked (destination)
							square_selected = (row, col)
							player_clicks.append(square_selected)

						if len(player_clicks) == 2: # 'from' and 'to' are available
							move = Move(player_clicks[0], player_clicks[1], gs.board) # create move object

							if move in valid_moves:

								gs.make_move(move)
								animate(move, screen, gs.board, clock)
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
											gs.board[move.end_row][move.end_col] = userDb + move.piece_moved[1]
											master.destroy()
											break
								print(move.get_chess_notation())

								square_selected = ()
								player_clicks = []

							else:
								current_turn = "l" if gs.light_to_move else "d"
								if current_turn == first_click_turn:
									player_clicks = [square_selected]
									square_selected = ()
								else:
									player_clicks = []
									square_selected = ()
					if gs.is_check_mate: # if one player win
						mbox.showinfo("CHECKMATE", "DARK TEAM WINS")
					if gs.is_stalemate: #if drawn
						mbox.showinfo("STALEMATE", "IT IS A STALEMATE")
		display_game_state(screen, gs, valid_moves, player_clicks)
		clock.tick(MAX_FPS)
		pg.display.flip()


def evaluation_function(board):
	end_game = True
	for i in range(len(board)):
		for k in range(len(board)):
			if board[i][k] == "ql" or "qd":
				end_game = False
				break
	piece_values = {"p": 100, "n": 320, "b": 330, "r": 500, "q": 900, "k": 20000}
	light_pawn_pst = [
		[0, 0, 0, 0, 0, 0, 0, 0],
		[50, 50, 50, 50, 50, 50, 50, 50],
		[10, 10, 20, 30, 30, 20, 10, 10],
		[5, 5, 10, 25, 25, 10, 5, 5],
		[0, 0, 0, 20, 20, 0, 0, 0],
		[5, -5, -10, 0, 0, -10, -5, 5],
		[5, 10, 10, -20, -20, 10, 10, 5],
		[0, 0, 0, 0, 0, 0, 0, 0]]
	dark_pawn_pst = light_pawn_pst[::-1]

	light_knight_pst = [
		[-50, -40, -30, -30, -30, -30, -40, -50],
		[-40, -20, 0, 0, 0, 0, -20, -40],
		[-30, 0, 10, 15, 15, 10, 0, -30],
		[-30, 5, 15, 20, 20, 15, 5, -30],
		[-30, 0, 15, 20, 20, 15, 0, -30],
		[-30, 5, 10, 15, 15, 10, 5, -30],
		[-40, -20, 0, 5, 5, 0, -20, -40],
		[-50, -40, -30, -30, -30, -30, -40, -50]]
	dark_knight_pst = light_knight_pst[::-1]

	light_bishop_pst = [
		[-20, -10, -10, -10, -10, -10, -10, -20],
		[-10, 0, 0, 0, 0, 0, 0, -10],
		[-10, 0, 5, 10, 10, 5, 0, -10],
		[-10, 5, 5, 10, 10, 5, 5, -10],
		[-10, 0, 10, 10, 10, 10, 0, -10],
		[-10, 10, 10, 10, 10, 10, 10, -10],
		[-10, 5, 0, 0, 0, 0, 5, -10],
		[-20, -10, -10, -10, -10, -10, -10, -20]]
	dark_bishop_pst = light_bishop_pst[::-1]

	light_rook_pst = [
		[0, 0, 0, 0, 0, 0, 0, 0],
		[5, 10, 10, 10, 10, 10, 10, 5],
		[-5, 0, 0, 0, 0, 0, 0, -5],
		[-5, 0, 0, 0, 0, 0, 0, -5],
		[-5, 0, 0, 0, 0, 0, 0, -5],
		[-5, 0, 0, 0, 0, 0, 0, -5],
		[-5, 0, 0, 0, 0, 0, 0, -5],
		[0, 0, 0, 5, 5, 0, 0, 0]]
	dark_rook_pst = light_rook_pst[::-1]

	light_queen_pst = [
		[-20, -10, -10, -5, -5, -10, -10, -20],
		[-10, 0, 0, 0, 0, 0, 0, -10],
		[-10, 0, 5, 5, 5, 5, 0, -10],
		[-5, 0, 5, 5, 5, 5, 0, -5],
		[0, 0, 5, 5, 5, 5, 0, -5],
		[-10, 5, 5, 5, 5, 5, 0, -10],
		[-10, 0, 5, 0, 0, 0, 0, -10],
		[-20, -10, -10, -5, -5, -10, -10, -20]]
	dark_queen_pst = light_queen_pst[::-1]

	if end_game:
		light_king_pst = [
			[-50, -40, -30, -20, -20, -30, -40, -50],
			[-30, -20, -10, 0, 0, -10, -20, -30],
			[-30, -10, 20, 30, 30, 20, -10, -30],
			[-30, -10, 30, 40, 40, 30, -10, -30],
			[-30, -10, 30, 40, 40, 30, -10, -30],
			[-30, -10, 20, 30, 30, 20, -10, -30],
			[-30, -30, 0, 0, 0, 0, -30, -30],
			[-50, -30, -30, -30, -30, -30, -30, -50]]
	else:
		light_king_pst = [
			[-30, -40, -40, -50, -50, -40, -40, -30],
			[-30, -40, -40, -50, -50, -40, -40, -30],
			[-30, -40, -40, -50, -50, -40, -40, -30],
			[-30, -40, -40, -50, -50, -40, -40, -30],
			[-20, -30, -30, -40, -40, -30, -30, -20],
			[-10, -20, -20, -20, -20, -20, -20, -10],
			[20, 20, 0, 0, 0, 0, 20, 20],
			[20, 30, 10, 0, 0, 10, 30, 20]]
	dark_king_pst = light_king_pst[::-1]
	light_pawn_num, light_pawn_ind = 0, []
	dark_pawn_num, dark_pawn_ind = 0, []
	light_knight_num, light_knight_ind = 0, []
	dark_knight_num, dark_knight_ind = 0, []
	light_bishop_num, light_bishop_ind = 0, []
	dark_bishop_num, dark_bishop_ind = 0, []
	light_rook_num, light_rook_ind = 0, []
	dark_rook_num, dark_rook_ind = 0, []
	light_queen_num, light_queen_ind = 0, []
	dark_queen_num, dark_queen_ind = 0, []
	light_king_ind = []
	dark_king_ind = []
	# color = "l" if gs.light_to_move else "d"
	for i in range(len(board)):
		for j in range(len(board)):
			if board[i][j] == "  ":
				continue
			elif board[i][j] == "pl":
				light_pawn_num += 1
				light_pawn_ind.append((i, j))
			elif board[i][j] == "pd":
				dark_pawn_num += 1
				dark_pawn_ind.append((i, j))
			elif board[i][j] == "nl":
				light_knight_num += 1
				light_knight_ind.append((i, j))
			elif board[i][j] == "nd":
				dark_knight_num += 1
				dark_knight_ind.append((i, j))
			elif board[i][j] == "bl":
				light_bishop_num += 1
				light_bishop_ind.append((i, j))
			elif board[i][j] == "bd":
				dark_bishop_num += 1
				dark_bishop_ind.append((i, j))
			elif board[i][j] == "rl":
				light_rook_num += 1
				light_rook_ind.append((i, j))
			elif board[i][j] == "rd":
				dark_rook_num += 1
				dark_rook_ind.append((i, j))
			elif board[i][j] == "ql":
				light_queen_num += 1
				light_queen_ind.append((i, j))
			elif board[i][j] == "qd":
				dark_queen_num += 1
				dark_queen_ind.append((i, j))
			elif board[i][j] == "kl":
				light_king_ind.append((i, j))
			elif board[i][j] == "kd":
				dark_king_ind.append((i, j))
	light_material = (piece_values["p"] * light_pawn_num + piece_values["n"] * light_knight_num + piece_values["r"] * light_rook_num +
					  piece_values["b"] * light_bishop_num + piece_values["q"] * light_queen_num + piece_values["k"])
	dark_material = (piece_values["p"] * dark_pawn_num + piece_values["n"] * dark_knight_num + piece_values["r"] * dark_rook_num +
					 piece_values["b"] * dark_bishop_num + piece_values["q"] * dark_queen_num + piece_values["k"])
	light_pawnpst_material = sum(light_pawn_pst[i[0]][i[1]] for i in light_pawn_ind)
	dark_pawnpst_material = sum(dark_pawn_pst[i[0]][i[1]] for i in dark_pawn_ind)
	light_knightpst_material = sum(light_knight_pst[i[0]][i[1]] for i in light_knight_ind)
	dark_knightpst_material = sum(dark_knight_pst[i[0]][i[1]] for i in dark_knight_ind)
	light_bishoppst_material = sum(light_bishop_pst[i[0]][i[1]] for i in light_bishop_ind)
	dark_bishoppst_material = sum(dark_bishop_pst[i[0]][i[1]] for i in dark_bishop_ind)
	light_rookpst_material = sum(light_rook_pst[i[0]][i[1]] for i in light_rook_ind)
	dark_rookpst_material = sum(dark_rook_pst[i[0]][i[1]] for i in dark_rook_ind)
	light_queenpst_material = sum(light_queen_pst[i[0]][i[1]] for i in light_queen_ind)
	dark_queenpst_material = sum(dark_queen_pst[i[0]][i[1]] for i in dark_queen_ind)
	light_kingpst_material = sum(light_king_pst[i[0]][i[1]] for i in light_king_ind)
	dark_kingpst_material = sum(dark_king_pst[i[0]][i[1]] for i in dark_king_ind)
	total_light_pst_material = (
				light_pawnpst_material + light_knightpst_material + light_bishoppst_material + light_rookpst_material +
				light_queenpst_material + light_kingpst_material)
	total_dark_pst_material = (
				dark_pawnpst_material + dark_knightpst_material + dark_bishoppst_material + dark_rookpst_material +
				dark_queenpst_material + dark_kingpst_material)
	total_light_material = light_material + total_light_pst_material
	total_dark_material = dark_material + total_dark_pst_material
	return total_light_material - total_dark_material

def alphabeta(board, best_move, depth, alpha, beta):
	gs = Game_state()
	if depth == 0:# or gs.is_check_mate() or gs.is_stalemate():
		return evaluation_function(board), best_move
	else:
		if gs.light_to_move:
			best_move = None
			for move in gs.get_valid_moves(Move):
				gs.make_move(move)
				alpha = evaluation_function(board)
				print(alpha)
				gs.light_to_move = False
				beta = evaluation_function(board)
				print(beta)
				gs.light_to_move = True
				score, move = alphabeta(board, best_move, depth - 1, alpha, beta)
				#print(score)
				if score > alpha:
					alpha = score
					best_move = move
					if alpha >= beta:
						break
				gs.undo_move(look_ahead_mode=True)
			return alpha, best_move
		else:
			best_move = None
			for move in gs.get_valid_moves(Move):
				gs.make_move(move)
				alpha = evaluation_function(board)
				gs.light_to_move = True
				beta = evaluation_function(board)
				gs.light_to_move = False
				score, move = alphabeta(board, perspective, depth - 1, alpha, beta)
				if score > beta:
					beta = score
					best_move = move
					if alpha >= beta:
						break
				gs.undo_move(look_ahead_mode=True)
			return beta, best_move

def display_game_state(screen, gs, valid_moves, player_clicks):
	"""
		display all graphics
	"""

	display_board(screen) # draw board squares

	highlight_square(screen, gs, valid_moves, player_clicks) # colorize highlighted squares

	display_pieces(screen, gs.board)
	display_ranks_files(screen)

def display_board(screen):
	"""
		display chess squares on board
	"""
	for rows in range(DIMENSION):
		for cols in range(DIMENSION):
			color = COLORS[(rows + cols) % 2]
			pg.draw.rect(screen, color, pg.Rect(cols*SQ_SIZE + BORDER//2, rows*SQ_SIZE + BORDER//2, SQ_SIZE, SQ_SIZE))


def display_pieces(screen, board):
	"""
		 display chess pieces on board from current game state
	"""
	for rows in range(DIMENSION):
		for cols in range(DIMENSION):
			piece = board[rows][cols]
			if piece != "  ":
				screen.blit(IMAGES[piece], pg.Rect(cols*SQ_SIZE + BORDER//2, rows*SQ_SIZE + BORDER//2, SQ_SIZE, SQ_SIZE))


def display_ranks_files(screen):
	"""
		display ranks (numbers) and files (letters) around board
	"""
	myfont = pg.font.SysFont("Liberation", 50)
	letters = ("a", "b", "c", "d", "e", "f", "g", "h")

	for index, file in enumerate(letters):
		file_surface = myfont.render(file, 0, (0, 0, 0))
		screen.blit(file_surface, (((index+1) * SQ_SIZE)+SQ_SIZE//4, SQ_SIZE//3))
		screen.blit(file_surface, (((index+1) * SQ_SIZE)+SQ_SIZE//4, (9*SQ_SIZE) + SQ_SIZE//8))
		
	
	for index, rank in enumerate(range(8, 0, -1)):
		rank_surface = myfont.render(str(rank), 0, (0, 0, 0))
		screen.blit(rank_surface, (SQ_SIZE//2, ((index+1) * SQ_SIZE)+SQ_SIZE//4))
		screen.blit(rank_surface, ((9*SQ_SIZE) + SQ_SIZE//4, ((index+1) * SQ_SIZE)+SQ_SIZE//4))


def highlight_square(screen, gs, valid_moves, player_clicks):
	"""
		colorize selected pieces and valid moves
	"""
	if player_clicks != []:
		r, c = player_clicks[0]
		if gs.board[r][c][1] == ("l" if gs.light_to_move else "d"):

			# highlight selected square
			s = pg.Surface((SQ_SIZE, SQ_SIZE))
			s.set_alpha(140) # transparency value between 0 and 255 (transparent and opaque)
			s.fill(pg.Color("darkblue"))
			screen.blit(s, (c*SQ_SIZE + BORDER//2, r*SQ_SIZE + BORDER//2))

			# highlight valid moves
			s.fill(pg.Color("chartreuse"))
			for move in valid_moves:
				if move.start_row == r and move.start_col == c:
					screen.blit(s, (move.end_col*SQ_SIZE + BORDER//2, move.end_row*SQ_SIZE + BORDER//2))


def play_sound(move):
	"""
		plays move and captured sounds
	"""
	if move.piece_captured == "  ":
		pg.mixer.Sound.play(SOUND[0])
	else:
		pg.mixer.Sound.play(SOUND[1])


def animate(move, screen, board, clock):
	"""
		creates moving animation for chess pieces
	"""
	frames_per_square = 10 # frames for a single square move
	dr = move.end_row - move.start_row # total rows  to move
	dc = move.end_col - move.start_col # total column to move

	frame_count = int((dr**2 + dc**2)**0.5 * frames_per_square)
	sound_played = False
	for frame in range(frame_count+1):
		

		r, c = ((move.start_row + dr*frame/frame_count+0.01, move.start_col + dc*frame/frame_count+0.01))

		# play sound 
		if not sound_played and ((abs(move.end_row - r) + abs(move.end_col - c))/max((move.end_row+move.end_col + 0.01), (r+c + 0.01))) < 0.4:
			play_sound(move)
			sound_played = True



		display_board(screen)
		display_pieces(screen, board)

		# erase piece from destination square
		color = COLORS[(move.end_row + move.end_col) % 2]
		end_square = pg.Rect(move.end_col*SQ_SIZE + BORDER//2, move.end_row*SQ_SIZE + BORDER//2, SQ_SIZE, SQ_SIZE)
		pg.draw.rect(screen, color, end_square)

		# draw captured piece if any onto rectangle
		if move.piece_captured != "  ":
			 screen.blit(IMAGES[move.piece_captured], end_square)

		# draw moving piece
		screen.blit(IMAGES[move.piece_moved], pg.Rect(c*SQ_SIZE + BORDER//2, r*SQ_SIZE + BORDER//2, SQ_SIZE, SQ_SIZE))
		pg.display.flip()
		clock.tick(60)

if __name__ == "__main__":
	main()
