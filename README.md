![Chess Board AI Mode](/misc/Chess.gif)\

# STEAM CHESS ENGINE

## DESCRIPTION

**STEAM CHESS ENGINE** (named after Steamledge), is a Chess engine focused on Artificial Intelligence written in Python (using python 3.7.7 and pygame 1.9.6).  The engine has five files `main_menu.py`, `menu.py`, `main.py`, `engine.py` and `ai.py`.

### Features

*	GUI using pygame with a display resolution of 600 x600
*	Sounds for both piece moves and piece captures
*	Voice commentary for both moves, stalemate and checkmate
*	Square highlighting
*	Interactive menu for easy access to each mode
*	AI mode
*	Game playback after checkmate or stale (Human vs Human mode only)
*	Minimax algorithm w/ Alpha-beta pruning.
*	Move ordering based off heuristics (captures, promotions, e.t.c)
*	Efficient board evaluation function

### Game Modes

*	Human Vs Human
*	AI Vs AI

# CODE DESCRIPTION

Composed of five files:
The `main_menu.py` is the main menu of the game, where user chooses between offline and online (in progress) modes
The `menu.py` serves as an interface between the `main_menu.py` and `main.py`, connecting both files and providing the user with options to the various game modes available
The `main.py` file is the GUI of the engine using pygame to display the chess board, chess pieces as well as the game simulation. 
The `engine.py` creates the chess objects (board, pieces, moves e.t.c) and their functionalities.
The `ai.py` programs our AI bot. below is a detail description of each file


## main_menu.py (GUI)

This is the file to be run to start steam-chess. It uses the pygame module to display the menu window
*	`option_format`: displays the option to choose from
*	`menu`: functions that  displays the whole windows, captures events by user and links user to the menu 

## menu.py (GUI)

This links the `main_menu.py` with `main.py` (The chess board). it provides options on the various game modes to choose from.
*	`display_main`: This function displays the main board (`main.py`) with the appropriate mode selected by the user (Human vs Human or AI vs AI)
*	`player_format`: adds options to prompt users choice
*	`main_menu`: displays the menu window, captures user events and links to main

## main.py (GUI)

This is the GUI displaying all aspects of the chess game and handling user inputs. it contains the `main()` function which displays the chess game using pygame with the help of these supporting functions:
*	`display_game_state` :display all graphics
*	`display_board`: display chess squares on board
*	`display_pieces`:  display chess pieces on board from current game state
*	`display_ranks_files` :display ranks (numbers) and files (letters) around board
*	`play_sound`: plays 'move' and 'capture' sounds
*	`animate`: creates moving animations for chess pieces:
*	`get_chess_notation`: makes the voice commentary of moves, checkmate and stalemate

## engine.py (Heart of the Chess Engine)

This implements the rules of the game and stores the state of the chess board, including its pieces and moves. It has two Classes `Game_state` and `Move`. Each Class has a specific function:

### Game_state

* `self.board`: 8 X 8 dimensional array (Matrix of 8 rows and 8 columns ) i.e a list of lists. Each element of the Matrix  is a string of two characters representing the chess pieces in the order "type" + "colour".. light pawn = “pl” dark pawn = “pd” and empty square = "  " double empty space.
*	`get_pawn_moves`, `get_rook_moves`, `get_knight_moves`, `get_queen_moves`, `get_king_moves` and `get_bishop_moves` : this functions Calculates all possible moves for a given color (light or dark) and appends them to a list. This includes all types of chess moves, capture, castling and enpassant
*	`make_move`: moves pieces on the board from one square to another
*	`undo_move`: this undo moves made in the by using the move_log that saves all moves done
*	`get_all_possible_moves`: this gives naive possible moves of pieces on the board without taking checks into account
*	`get_valid_moves`: gives the valid piece moves on the board while considering potential checks

### Move:

A Move class abstracting all parameters needed for moving chess pieces on the board
*	`self.start_row`: row location of piece to be moved
*	`self.start_col`: column location of piece to be moved
*	`self.end_row`: intended row destination of piece to be moved
*	`self.end_col`: intended column destination of piece to be moved
*	`self.piece_moved`: actual piece moved
*	`self.piece_captured`: opponent piece if any on the destination square

## ai.py (AI Bot(s))

Included in the `ai.py` is the Minimax functions, which utilizes the MiniMax algorithm to evaluate board states. The MiniMax algorithm provided comes with alpha-beta pruning, move ordering. Some of the functions are:

*	`Evaluation`: this function evaluates the board at a given game state. It sums up the pieces on the board using piece values and also adds piece-square tables, which alter the value of a piece depending on which square it sits on.
*	`Minimax`: Minimax is a search algorithm that finds the next optimal move by minimizing the potential loss in a worst case scenario. This algorithm was adapted from Sebastian Lague’s Algorithms Explained – minimax and alpha-beta pruning. It uses the evaluation function to determine the best possible move to win the game. The Minimax was made better using the alpha beta pruning, This significantly reduces the number of moves required to be generated hence increasing search speed without affecting the outcome
*	`Move_ordering`: this function helps the ai to order moves base on importance (capture, promotion, defending the king) this helps to further assist in choosing the best move without making unnecessary sacrifices.
*	`light_pieces and dark_pieces`: These are dictionaries containing all the pieces at a particular game state which makes for faster static evaluation of the board. It is updated on the fly as moves and captures are being made
*	`update_pieces_dictionaries`: This updates light_pieces and dark_pieces during the hidden simulation in the minimax algorithm. It creates a copy of the dictionary to be used by the minimax during tree search for best move.
*	`ai_light_move` and `ai_dark_move`: this serves as a plug for the ai to make moves generated using the minimax algorithm on the board. It also updates the light_pieces and dark_pieces dictionary
*	`ai_move`: determines the turn for both team's AI also saves a running memory of the board state with moves and captures
*	`ai_reset`: resets the light pieces and dark pieces dictionaries when AI mode is activated/deactivated (in case moves were made outside AI mode)

## HOW TO PLAY

### Installation:

*	Clone/Download and extract repo in a folder on your system
*	Create and activate an environment

	- __Linux__ or __Mac__:
	```
	conda create -n chess python=3
	source activate chess
	```
	- __Windows__:
	```
	conda create --name chess python=3
	activate chess
	```
*	Install pygame from within chess environment
	`pip install pygame`
*	Install pyttsx3  from within chess environment
	`pip install pyttsx3`
*	Start game by running the following command:
- __Linux__ or __Mac__:
```
py main_menu.py
```
- __Windows__:
````
python main_menu.py
````

## USER INPUTS

*	Double click mouse-left to select options in the menu window
*	Press “R” on keyboard to reset game (only human vs human mode)
*	Press “U” on keyboard to undo move made (only human vs human mode)
*	Mouse left click on piece and square to select piece and make move respectively (only human vs human mode)
*	Press "M" to mute commentary during game play
*	Press "P" after end of game (`stalemate` or `checkmate`) to playback the entire game move by move. press "N" to toggle next move and "B" for previous move

## LIMITATIONS:

*	The AI sometimes finds it hard to make checkmates at sufficiently complex end-game scenarios. This can be overcome by providing a separate group of piece-square tables for end-games
*	Minimax search depth is currently set to 3 (higher search values take more than 10 seconds per move)
*	No Human Vs AI mode
