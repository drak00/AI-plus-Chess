##This is the GUI displaying all aspects of the chess game and 
##handling user inputs

import pygame as pg
from engine import Game_state, Move
from tkinter import messagebox as mbox

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
		if gs.is_check_mate: # if one player wins
			if gs.light_to_move:
				mbox.showinfo("CHECKMATE", "LIGHT TEAM WINS")
			else:
				mbox.showinfo("CHECKMATE", "DARK TEAM WINS")
		if gs.is_stalemate: #if drawn
			mbox.showinfo("STALEMATE", "IT IS A STALEMATE")
		display_game_state(screen, gs, valid_moves, player_clicks)
		clock.tick(MAX_FPS)
		pg.display.flip()


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
