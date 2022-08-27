import pygame as pg
from ai import ai_move, ai_reset
from menu import main_menu
import random
import sys

# Game Initialization
pg.init()

# canvas for displaying menu
window = (600, 600)
screen=pg.display.set_mode(window)
font = pg.font.SysFont("Helvetica",50)

# useful predefined Colours
white = pg.Color("ghostwhite")
brown = (66,44,22)
green = pg.Color("chartreuse")
yellow = pg.Color("Peru")
bg_color = pg.Color("chartreuse")
red = (255,0,0)

# Game Framerate
clock = pg.time.Clock()
FPS=30


def canvas_obj(obj_type = "text", obj_message = "", obj_size = 100, 
               obj_colour = yellow, obj_loc = None):

    """
        creates canvas object for pg window canvas
        supported objects:
            * image
            * text

        obj_loc ==> path to image

    """

    if obj_type == "text":
        return font.render(obj_message, obj_size, obj_colour)
    elif obj_type == "image":
        return pg.transform.scale(pg.image.load(obj_loc), (obj_size, obj_size))

def toggle(text, loc):
    """
        toggles black and white side selection text and image
    """
    if (text, loc) == ("< White >", "images/pl.png"):
        return ("< Black >", "images/pd.png")
    else:
        return ("< White >", "images/pl.png")

# Main Menu
def menu():

    title = canvas_obj(obj_type = "text", obj_message = "CHESS AI PLATFORM",
                       obj_size = 100)

    bg_pix = canvas_obj(obj_type  = "image", 
                         obj_loc = "images/ChessMenu.png",
                         obj_size = 640)

    pawn_pix = canvas_obj(obj_type = "image", 
                          obj_loc = "images/pl.png",
                          obj_size = 60)

    side_text, pawn_loc = ("< White >", "images/pl.png")
 
    choice, mode = None, None
    pg.mixer.Sound.play(pg.mixer.Sound("audio/The-Soul-Chamber.wav"))

    while True:
        for event in pg.event.get():
            if event.type==pg.QUIT:
                pg.quit()

           # Navigate menu
            if event.type == pg.MOUSEBUTTONDOWN:
                a, b  = pg.mouse.get_pos()

                if (60 <= a <= 330) and (200<= b <=230):
                    mode = choice if choice == "select side" else None
                    choice = "select side"
                                               
                elif (60 <= a <= 300) and (300<= b <=330):
                    mode = choice if choice == "offline" else None
                    choice = "offline"
                        
                elif (60 <= a <= 300) and (400<= b <=430):
                    mode = choice if choice == "online" else None
                    choice = "online"

                elif (460 <= a <= 550) and (500<= b <=530):
                    mode = choice if choice == "quit" else None
                    choice = "quit"
        
        
        if choice not in  ["select side", "quit"] and\
        mode not in  ["select side", "quit"]:

            colour_offline = brown if mode == "offline" else\
                    green if choice == "offline" else white

            colour_online = brown if mode == "online" else\
                    green if choice == "online" else white
            
            quit_colour = white

            #main_menu()
            #mode=""
            #option=""

        elif choice == "select side":
            if mode == choice:
                side_text, pawn_loc = toggle(side_text, pawn_loc)
                mode = None            
                    
        elif choice == "quit":
            quit_colour = red
            if mode == choice:
                pg.time.delay(500)
                pg.quit()
        
        print(side_text, pawn_loc)

        select_side_text = canvas_obj(obj_type = "text", obj_size = 75, 
                                     obj_colour = yellow, obj_message = side_text)

        select_side_pix = canvas_obj(obj_type = "image", obj_loc = pawn_loc,
                                        obj_size = 100)

        offline_text  = canvas_obj(obj_type = "text", obj_size = 75, 
                                     obj_colour = colour_offline, obj_message = "OFFLINE")

        online_text  = canvas_obj(obj_type = "text", obj_size = 75, 
                                     obj_colour = colour_online, obj_message = "ONLINE")

        
        quit_text = canvas_obj(obj_type = "text", obj_message = "QUIT",
                              obj_size = 75, obj_colour = quit_colour)
        
        screen.blit(bg_pix, (0,1))
        screen.blit(select_side_pix, (250,200))  
        screen.blit(title, ( 60 , 30))
        screen.blit(select_side_text, (60, 200))
        screen.blit(offline_text, (60, 300))
        screen.blit(online_text, (60, 400))
        screen.blit(quit_text, (462, 500))
        
        
        pg.display.update()
        clock.tick(FPS)
        pg.display.set_caption("CHESS AI PLATFORM")    

#Initialize the Game
menu()
pg.quit()
quit()
