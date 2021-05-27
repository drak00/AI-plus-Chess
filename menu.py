import pygame as pg
from ai import ai_move, ai_reset
from engine import Game_state, Move
import random
import sys

# Game Initialization
pg.init()

# menu Resolution
screen_width=600
screen_height=600
screen=pg.display.set_mode((screen_width, screen_height))
font = pg.font.SysFont("Helvetica",75)

#Game resolution

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
FLIP = sys.argv[1] if len(sys.argv) == 2 else False # dark starts first if arg passed  

def load_images(): #work I can learn how to add image from here
	"""
		loads images from directory into dictionary with parameters SQ_SIZE and OFFSET
	"""

	pieces = ["bd", "bl", "kd", "kl", "nd", "nl", "pd", "pl", "qd", "ql", "rd", "rl"]

	for piece in pieces:
		IMAGES[piece] = pg.transform.scale(pg.image.load("images/"+ piece + ".png"), (SQ_SIZE - OFFSET, SQ_SIZE - OFFSET))
		IMAGES2[piece] = pg.transform.scale(pg.image.load("images/"+ piece + ".png"), (32, 32))


# player Renderer
def player_format(message, playerSize, playerColor):
	newplayer=font.render(message, 0, playerColor)
	return newplayer
# Colors
white=pg.Color("ghostwhite")
black=(0, 0, 0)
gray=(50, 50, 50)
brown=(66,44,22)
green=pg.Color("chartreuse")
blue=(0, 0, 255)
yellow=pg.Color("Peru")
bg_color=pg.Color("chartreuse")
red=(255,0,0)
font = pg.font.SysFont("Liberation", 50)
 
# Game Framerate
clock = pg.time.Clock()
FPS=30


# Main Menu
def main_menu():
 
	menu=True
	selected=""
	mode=""
	screen = pg.display.set_mode((WIDTH + BORDER, HEIGHT + BORDER))
	#screen.fill(pg.Color("ghostwhite"))
	screen.fill(pg.Color("Peru"))

	while menu:
		for event in pg.event.get():
			if event.type==pg.QUIT:
				pg.quit()
				quit()

		   #selecting menu Items
			if event.type == pg.MOUSEBUTTONDOWN:
				(mouseX, mouseY) = pg.mouse.get_pos()
				a,b=mouseX,mouseY
				if (60 <= a <= 330) and (200<=b<=230):
					if selected !="player1":
						selected="player1"
					elif selected =="player1":
						mode="player1"
						print("selected earlier")    
				elif (60 <= a <= 300) and (300<=b<=330):
					if selected !="player2":
						selected="player2"
					elif selected =="player2":
						mode="player2"
						print("selected earlier 2") 
				elif (60 <= a <= 200) and (400<=b<=430):
					if selected !="aimode":
						selected="aimode"
					elif selected =="aimode":
						mode="aimode"
						print("selected earlier ai") 
				elif (460 <= a <= 550) and (500<=b<=530):
					if selected !="quit":
						selected="quit"
					elif selected =="quit":
						mode="quit"
						print("selected quit") 
		# Main Menu UI
		# screen.fill(yellow)
		title=player_format("CHESS", 100, yellow)
		name=pg.transform.scale(pg.image.load("images/menu.jfif"),(640,640)) #background image

		#selections and event trigger
		if selected=="player1":
			player_start=player_format("SINGLE PLAYER",  75, green)
			if mode=="player1":
				player_start = player_format("SINGLE PLAYER", 75, brown)

		else:
			player_start = player_format("SINGLE PLAYER", 75, white)
			
		if selected=="player2":
			player2_start=player_format("TWO PLAYERS",  75, green)
			if mode=="player2":
				player2_start = player_format("TWO PLAYER", 75, brown)
		else:
			player2_start = player_format("TWO PLAYERS", 75, white)  

		if selected=="aimode":
			if mode!="aimode":
				player_ai=player_format("AI MODE",  75, green)
			elif mode=="aimode":
				player_ai = player_format("AI MODE", 75, brown)
		else:
			player_ai = player_format("AI MODE", 75, white) 
	
		if selected=="quit":
			player_quit=player_format("QUIT",  75, red)
			if mode=="quit":
				pg.time.delay(500)
				quit()   
		else:
			player_quit = player_format("QUIT", 75, white)

		   
 
	   
		# Main Menu player

		screen.blit(name, (0,1))
		screen.blit(title, ( 60 , 30))
		screen.blit(player_start, (60, 200))
		screen.blit(player2_start, (60, 300))
		screen.blit(player_ai, (60, 400))
		screen.blit(player_quit, (462, 500))
		
		
		pg.display.update()
		clock.tick(FPS)
		pg.display.set_caption("CHESS")	

#Initialize the Game
main_menu()
pg.quit()
quit()