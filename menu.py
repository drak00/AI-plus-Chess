import pygame as pg
from main import main

# Game Initialization
pg.init()

# menu Resolution
screen_width=600
screen_height=600
screen=pg.display.set_mode((screen_width, screen_height))
font = pg.font.SysFont("Helvetica",75)
#
def display_main(choice):
    """
        Link option To main board
    """
    pg.mixer.pause()
    return main(choice)


def player_format(message, player_size, player_color):
    """
        Add Menu Options
    """
    new_player=font.render(message, 0, player_color)
    return new_player
# Colors
white=pg.Color("ghostwhite")
black=(0, 0, 0)
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
def game_mode_selection(mode, player):
 
    menu=True
    selected=""
    mode=""


    player_start=player_format("SINGLE PLAYER",  75, white)
    player2_start = player_format("TWO PLAYER", 75, white)
    player_ai=player_format("AI MODE",  75, white)
    player_quit=player_format("BACK",  75, white)

    while menu:
        for event in pg.event.get():
            if event.type==pg.QUIT:
                pg.quit()
                quit()

           #selecting menu Items
            if event.type == pg.MOUSEBUTTONDOWN:
                (mouseX, mouseY) = pg.mouse.get_pos()
                a,b=mouseX,mouseY
                print("values are {} and {}".format(a, b))

                if (60 <= a <= 330) and (200<=b<=230):
                    if selected !="player1":
                        selected="player1"
                    elif selected =="player1":
                        mode="player1"
                           
                elif (60 <= a <= 300) and (300<=b<=330):
                    if selected !="player2":
                        selected="player2"
                    elif selected =="player2":
                        mode="player2"
                        
                elif (60 <= a <= 200) and (400<=b<=430):
                    if selected !="aimode":
                        selected="aimode"
                    elif selected =="aimode":
                        mode="aimode"
                         
                elif (460 <= a <= 550) and (500<=b<=530):
                    if selected !="quit":
                        selected="quit"
                    elif selected =="quit":
                        mode="quit"

                                        
        # Main Menu UI
        
        # screen.fill(yellow)
        title=player_format("CHESS AI PLATFORM", 100, yellow)
        name=pg.transform.scale(pg.image.load("images/ChessMenu.png"),(640,640)) #background image
        
        #selections and event trigger
        if selected=="player1":
            player_start=player_format("SINGLE PLAYER",  75, green)
            if mode=="player1":
                player_start = player_format("SINGLE PLAYER", 75, brown)

            else:
                player_start = player_format("SINGLE PLAYER", 75, white)
            
        if selected=="player2":
            print("player2")
            player2_start=player_format("TWO PLAYERS",  75, green)
            if mode=="player2":
                player2_start = player_format("TWO PLAYER", 75, brown)
                display_main(False)
                mode=""
                player=""
        else:
            print("entered else")
            player2_start = player_format("TWO PLAYERS", 75, white)  

        if selected=="aimode":
            if mode!="aimode":
                player_ai=player_format("AI MODE",  75, green)
            elif mode=="aimode":
                player_ai = player_format("AI MODE", 75, brown)
                display_main(True)
                mode=""
                player=""
                
        else:
            player_ai = player_format("AI MODE", 75, white) 
    
        if selected=="quit":
            player_quit=player_format("BACK",  75, red)
            if mode=="quit":
                mode=""
                player=""
                menu=False
                
       
    
                 
        else:
            player_quit = player_format("BACK", 75, white)

           
 
       
        # Main Menu player
        screen.blit(name, (0,1))
        screen.blit(title, ( 60 , 30))
        screen.blit(player_start, (60, 200))
        screen.blit(player2_start, (60, 300))
        screen.blit(player_ai, (60, 400))
        screen.blit(player_quit, (462, 500))
        
        
        pg.display.update()
        clock.tick(FPS)
        pg.display.set_caption("CHESS AI PLATFORM")    

#Initialize the Game
# main_menu()
# pg.quit()
# quit()
