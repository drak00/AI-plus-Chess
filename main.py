##This is the GUI displaying all aspects of the chess game and
##handling user inputs

import pygame as pg
from ai import ai_move, ai_reset
from engine import Game_state, Move
import random
import sys

pg.init()

BORDER = 128 # for the ranks and files
WIDTH = HEIGHT = 512 # of the chess board
DIMENSION = 8 # rows and columns
OFFSET = 5 # for image scaling
height = width = 64 # with for pawn promotion board
dimension = 2 # rows and clolums for pawn promotion board
square = height//2 # size of promotion piece sqaure

SQ_SIZE = HEIGHT // DIMENSION # size of each board square
MAX_FPS = 15
IMAGES = {}
IMAGES2 = {}
COLORS = [pg.Color("burlywood1"), pg.Color("darkorange4")] #work add colo
SOUND = [pg.mixer.Sound("audio/move.wav"), pg.mixer.Sound("audio/capture.wav")] #work
FLIP = sys.argv[1] if len(sys.argv) == 2 else False # dark starts first if arg passed # work on two players set true

def load_images(): #work I can learn how to add image from here
	"""
		loads images from directory into dictionary with parameters SQ_SIZE and OFFSET
	"""

	pieces = ["bd", "bl", "kd", "kl", "nd", "nl", "pd", "pl", "qd", "ql", "rd", "rl"]

	for piece in pieces:
		IMAGES[piece] = pg.transform.scale(pg.image.load("images/"+ piece + ".png"), (SQ_SIZE - OFFSET, SQ_SIZE - OFFSET))
		IMAGES2[piece] = pg.transform.scale(pg.image.load("images/"+ piece + ".png"), (32, 32))

def main():
	screen = pg.display.set_mode((WIDTH + BORDER, HEIGHT + BORDER))
	clock = pg.time.Clock()
	#screen.fill(pg.Color("ghostwhite"))
	screen.fill(pg.Color("Peru"))


	gs = Game_state()
	load_images()
	gs.light_to_move = not gs.light_to_move if FLIP else True #work set false for 2 playes
	running = True

	square_selected = () # x, y coordinate of selected square
	player_clicks = [] # list of appended square_selected
	valid_moves, first_click_turn = gs.get_valid_moves() # compute valid moves outside loop (for efficiency)
	game_over = False # signals end of game
	user_prompt = False # pauses gui rendering for user input
	AI_MODE = False # flag for activating AI mode
	delay = 0 # delay the speed of AI plays
	display_time = 0 # AI_MODE text display persistence timer

	while running:

		if not user_prompt:
			found = False

			if AI_MODE and display_time == 0 and not game_over:

				# pause a bit between AI plays if delay > 0
				if delay == 0:
					move, gs = ai_move(gs)

					if move: # if AI made a move
						animate(move, screen, gs.board, clock)
						print(move.get_chess_notation())
					delay = 20 # pause magnitude
				else:
					delay -= 1

			for e in pg.event.get():
				if e.type == pg.QUIT:
					running = False

				elif e.type == pg.KEYDOWN:
					if e.key == pg.K_u and not AI_MODE: # u key pressed (undo last move)
						gs.undo_move()
						valid_moves, first_click_turn = gs.get_valid_moves()

					elif e.key == pg.K_r and not AI_MODE: # r key pressed (reset game)
						gs = Game_state()
						valid_moves, turn = [], None
						square_selected = ()
						player_clicks = []
						print("Board reset!")
						valid_moves, first_click_turn = gs.get_valid_moves()

					elif e.key == pg.K_a: # a key pressed (toggle AI mode)
						#toggle = True
						display_time = 10
						AI_MODE = not AI_MODE
						ai_reset()
						print("AI MODE ENABLED") if AI_MODE else print("AI MODE DISABLED")



				elif e.type == pg.MOUSEBUTTONDOWN:

					if not game_over and not AI_MODE:

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

								for obj in range(len(valid_moves)):

									if move == valid_moves[obj]:
										move = valid_moves[obj]
										found = True

										gs.make_move(move)


										if (move.end_row == 0 or move.end_row == 7) and (move.piece_moved[0] == "p"):
											user_prompt = True
											choice = ("q", "r", "b", "n")
											promotion = True
											while promotion:
												for event in pg.event.get():
													if event.type == pg.MOUSEBUTTONDOWN:
														location = pg.mouse.get_pos() # x, y location of mouse click
														location_col_transform = location[0] // square- 1 # divided by sqaure size
														location_row_transform = location[1] // square - 1
														row_comb= [1,2,15,16] # list for all the possible rows
														if location_row_transform in row_comb:  #making sure the event meet requirements
															row = location_row_transform
															col =location_col_transform
															if ((row == 15) and (col%2 != 0)) or ((row == 1) and (col%2 != 0)):
																piece = "q"
															elif ((row == 15) and (col%2 == 0)) or ((row == 1) and (col%2 == 0)):
																piece = "r"
															elif ((row == 16) and (col%2 != 0)) or ((row == 2) and (col%2 != 0)):
																piece = "b"
															elif ((row == 16) and (col%2 == 0)) or ((row == 2) and (col%2 == 0)):
																piece = "n"
															print("Promoting Piece")
															promotion = False
												display_board2(screen,move.end_row, move.end_col)
												pg.display.update()
												clock.tick(5)

											gs.board[move.end_row][move.end_col] = piece+ move.piece_moved[1]
											user_prompt = False

										animate(move, screen, gs.board, clock)

										print(move.get_chess_notation())

										square_selected = ()
										player_clicks = []
										valid_moves, first_click_turn = gs.get_valid_moves()
										break

								if not found: # move selected not a valid move

									current_turn = "l" if gs.light_to_move else "d"
									if current_turn == first_click_turn:
										player_clicks = [square_selected]
										square_selected = ()
									else:
										player_clicks = []

										square_selected = ()

		display_game_state(screen, gs, valid_moves, player_clicks)

		# display text for switching AI mode
		if display_time > 0:
			display_text(screen, "AI MODE ENABLED", "Green") if AI_MODE else display_text(screen, "AI MODE DISABLED", "Red")
			display_time -= 1 # countdown for text to disappear

		if AI_MODE and not game_over:
			if gs.light_to_move:
				display_Thinking_text(screen,gs, "Thinking....")
			else:
				display_Thinking_text(screen, gs, "Thinking....")
		if gs.check_mate:
			game_over = True

			if gs.light_to_move:
				display_text(screen, "Dark wins by checkmate")
			else:
				display_text(screen, "Light wins by checkmate")

		elif gs.stale_mate:
			game_over = True
			display_text(screen, "Stalemate")


		clock.tick(MAX_FPS)
		pg.display.flip()


def display_game_state(screen, gs, valid_moves, player_clicks): #work call my start menu here
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


def display_board2(screen, row, col):
	"""
		display new surface to promt user choice of promotion
	"""
	screen2 = pg.Surface((64,64))  # second screen (a surface to bliet pieces for choice)
	if row == 0:  #if light team
		piece = [["ql", "rl",], ["bl", "nl"]]
	else:  #if dark_team
		piece = [["qd", "rd",], ["bd", "nd"]]
	for rows in range(dimension):
		for cols in range(dimension):
			color = COLORS[(rows + cols) % 2]
			piec = piece[rows][cols]
			pg.draw.rect(screen2, color, pg.Rect(cols*square, rows*square, square, square))
			screen2.blit(IMAGES2[piec],pg.Rect(cols*square, rows*square, square, square))
			screen.blit(screen2, (col*SQ_SIZE + BORDER//2, row*SQ_SIZE + BORDER//2))



def display_pieces(screen, board):
	"""
		 display chess pieces on board from current game state
	"""
	for rows in range(DIMENSION):
		for cols in range(DIMENSION):
			piece = board[rows][cols]
			if piece != "  ":
				screen.blit(IMAGES[piece], pg.Rect(cols*SQ_SIZE + BORDER//2, rows*SQ_SIZE + BORDER//2, SQ_SIZE, SQ_SIZE))


def display_ranks_files(screen):#work read
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
	if player_clicks:
		r, c = player_clicks[0]
		if gs.board[r][c][1] == ("l" if gs.light_to_move else "d"):

			# highlight selected square
			s = pg.Surface((SQ_SIZE, SQ_SIZE))
			s.set_alpha(140) # transparency value between 0 and 255 (transparent and opaque)
			s.fill(pg.Color("darkblue"))
			screen.blit(s, (c*SQ_SIZE + BORDER//2, r*SQ_SIZE + BORDER//2)) #show the color

			# highlight valid moves
			s.fill(pg.Color("chartreuse"))
			for move in valid_moves:
				if move.start_row == r and move.start_col == c:
					screen.blit(s, (move.end_col*SQ_SIZE + BORDER//2, move.end_row*SQ_SIZE + BORDER//2))
					

	if gs.move_log:
		last_move = gs.move_log[-1]
		s = pg.Surface((SQ_SIZE, SQ_SIZE))
		s.set_alpha(90)
		s.fill(pg.Color("blue"))
		if  gs.board[last_move.end_row][last_move.end_col][1] == ("d" if gs.light_to_move else "l"):
			screen.blit(s, (last_move.end_col * SQ_SIZE + BORDER // 2, last_move.end_row * SQ_SIZE + BORDER // 2))
			screen.blit(s, (last_move.start_col * SQ_SIZE + BORDER // 2, last_move.start_row * SQ_SIZE + BORDER // 2))


def play_sound(move): #work
	"""
		plays move and captured sounds
	"""
	#print("sound"+str(move.en_passant_captured))
	if move.en_passant_captured:
		pg.mixer.Sound.play(SOUND[1])
	elif move.piece_captured == "  ":
		pg.mixer.Sound.play(SOUND[0])

	else:
		pg.mixer.Sound.play(SOUND[1])


def display_text(screen, text, color = None):

	font = pg.font.SysFont("Helvetica", 32, True, False)
	background = random.choice(("Red", "Green"))
	text_object = font.render(text, 0, pg.Color("Black" if color else background))

	text_location = pg.Rect(0, 0, WIDTH+BORDER, HEIGHT+BORDER).move((WIDTH+BORDER)//2 - text_object.get_width()/2, (HEIGHT+BORDER)//2 - text_object.get_height()/2)
	screen.blit(text_object, text_location)

	if not color:
		text_object = font.render(text, 0, pg.Color("Black"))
		screen.blit(text_object, text_location.move(2, 2))
	else:
		text_object = font.render(text, 0, pg.Color(color))
		screen.blit(text_object, text_location.move(2, 2))

def display_Thinking_text(screen, gs, text, color = None):

	font = pg.font.SysFont("Helvetica", 18, True, False)
	text_object = font.render(text, 0, pg.Color("Black"))
	if gs.light_to_move:
		text_location = pg.Rect(0,490, BORDER, BORDER).move((WIDTH+BORDER)//2 - text_object.get_width()/2, (BORDER)//2 - text_object.get_height()/2)
		screen.blit(text_object, text_location)
	else:
		text_location = pg.Rect(0,20, BORDER, BORDER).move((WIDTH+BORDER)//2 - text_object.get_width()/2, (BORDER)//2 - text_object.get_height()/2)
		screen.blit(text_object, text_location)
	if not color:
		text_object = font.render(text, 0, pg.Color("Red"))
		screen.blit(text_object, text_location.move(2, 2))
	else:
		text_object = font.render(text, 0, pg.Color(color))
		screen.blit(text_object, text_location.move(2, 2))


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


		r, c = ((move.start_row + dr*frame/frame_count, move.start_col + dc*frame/frame_count))

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
