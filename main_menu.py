import pygame as pg
from ai import ai_move, ai_reset
from menu import main_menu
import random
import sys

# Game Initialization
pg.init()

# menu Resolution
screen_width=600
screen_height=600
screen=pg.display.set_mode((screen_width, screen_height))
font = pg.font.SysFont("Helvetica",75)

def option_format(message, player_size, player_color):
	"""
		Add Menu Options
	"""
	new_option=font.render(message, 0, player_color)
	return new_option
# Colors
white=pg.Color("ghostwhite")
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
def menu():
 
	run=True
	selected=""
	mode=""

	while run:
		for event in pg.event.get():
			if event.type==pg.QUIT:
				pg.quit()
				quit()

		   #selecting menu Items
			if event.type == pg.MOUSEBUTTONDOWN:
				(mouseX, mouseY) = pg.mouse.get_pos()
				a,b=mouseX,mouseY
				if (60 <= a <= 330) and (200<=b<=230):
					if selected !="offline":
						selected="offline"
					elif selected =="offline":
						mode="offline"
						   
				elif (60 <= a <= 300) and (300<=b<=330):
					if selected !="online":
						selected="online"
					elif selected =="online":
						mode="online"
						
				elif (60 <= a <= 200) and (400<=b<=430):
					if selected !="side":
						selected="side"
					elif selected =="side":
						mode="side"
						 
				elif (460 <= a <= 550) and (500<=b<=530):
					if selected !="quit":
						selected="quit"
					elif selected =="quit":
						mode="quit"
						
		# Main Menu UI
		# screen.fill(yellow)
		title=option_format("STEAM CHESS ENGINE", 100, yellow)
		name=pg.transform.scale(pg.image.load("images/menu.jfif"),(640,640)) #quitground image
		pic=pg.transform.scale(pg.image.load("images/pl.png"),(60,60))

		#selections and event trigger
		if selected=="offline":
			option_start=option_format("OFFLINE",  75, green)
			if mode=="offline":
				option_start = option_format("OFFLINE", 75, brown)
				main_menu()
				mode=""
				option=""	

		else:
			option_start = option_format("OFFLINE", 75, white)
			
		if selected=="online":
			online_start=option_format("ONLINE",  75, green)
			if mode=="online":
				online_start = option_format("ONLINE", 75, brown)
				mode=""
				option=""
		else:
			online_start = option_format("ONLINE", 75, white)  

		if selected=="side":
			if mode!="side":
				option_side=option_format("< DARK >",  75, (0,0,0))
				pic=pg.transform.scale(pg.image.load("images/pd.png"),(60,60))

			elif mode=="side":
				option_side = option_format("< LIGHT >", 75, white)
				pic=pg.transform.scale(pg.image.load("images/pl.png"),(60,60))
				selected=""
				mode=""
				
		else:
			option_side = option_format("< LIGHT >", 75, white) 
	
		if selected=="quit":
			option_quit=option_format("QUIT",  75, red)
			if mode=="quit":
				pg.time.delay(500)
				quit()   
		else:
			option_quit = option_format("QUIT", 75, white)

		   
 
	   
		# Main Menu option

		screen.blit(name, (0,1))
		screen.blit(pic, (230,380))  
		screen.blit(title, ( 60 , 30))
		screen.blit(option_start, (60, 200))
		screen.blit(online_start, (60, 300))
		screen.blit(option_side, (60, 400))
		screen.blit(option_quit, (462, 500))
		
		
		pg.display.update()
		clock.tick(FPS)
		pg.display.set_caption("STEAM CHESS ENGINE")	

#Initialize the Game
menu()
pg.quit()
quit()