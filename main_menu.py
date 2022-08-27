import pygame as pg
from menu import game_mode_selection

# canvas for displaying menu
WINDOW = (600, 600)
screen=pg.display.set_mode(WINDOW)
font = pg.font.SysFont("Helvetica",50)

# useful predefined Colours
white = pg.Color("ghostwhite")
brown = (66,44,22)
green = pg.Color("chartreuse")
yellow = pg.Color("Peru")
dark = (90, 90, 90)
darker = (3, 3, 3)
red = (255,0,0)

# Game Framerate
clock = pg.time.Clock()
FPS=30


# Helpers
def canvas_obj(obj_type = "text", obj_message = "", obj_size = 100, 
               obj_colour = yellow, obj_loc = None, invert = False):

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
        img = pg.transform.scale(pg.image.load(obj_loc), (obj_size, obj_size))
        
        if invert:

            # convert background image pixels to gray for visibility
            # on main menu screen
            pg.PixelArray(img).replace((0, 0, 0), dark)
        return img

def toggle(text, loc, colour):
    """
        toggles black and white side selection text and image
    """
    if (text, loc, colour) == ("< White >", "images/pl.png", white):
        return ("< Black >", "images/pd.png", darker)
    else:
        return ("< White >", "images/pl.png", white)


# Main Menu
def offline_online_selection():

    player = "white"

    title = canvas_obj(obj_type = "text", obj_message = "CHESS AI PLATFORM",
                       obj_size = 100)

    bg_pix = canvas_obj(obj_type  = "image", 
                         obj_loc = "images/ChessMenu.png",
                         obj_size = 640)

    pawn_pix = canvas_obj(obj_type = "image", 
                          obj_loc = "images/pl.png",
                          obj_size = 60)

    side_text, pawn_loc, side_colour = ("< White >", "images/pl.png", white)
 
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

            if mode == "offline":
                game_mode_selection(mode, player)

        elif choice == "select side":
            if mode == choice:
                side_text, pawn_loc, side_colour = toggle(side_text, pawn_loc, side_colour)
                mode = None
                player = side_text.replace("< ", "").replace(" >", "")

                invert = True if side_text == "< Black >" else False
                bg_pix = canvas_obj(obj_type  = "image", 
                         obj_loc = "images/ChessMenu.png",
                         obj_size = 640, invert = invert)

        elif choice == "quit":
            quit_colour = red
            if mode == choice:
                pg.time.delay(500)
                pg.quit()
                quit()
        
        select_side_text = canvas_obj(obj_type = "text", obj_size = 75, 
                                     obj_colour = side_colour, obj_message = side_text)

        select_side_pix = canvas_obj(obj_type = "image", obj_loc = pawn_loc,
                                        obj_size = 100, invert = False)

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


if __name__ == "__main__":

    # Game Initialization
    pg.init()

    #Initialize the Game
    offline_online_selection()
    
