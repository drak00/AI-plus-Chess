![Chess Board AI Mode](/misc/Chess.gif)\

#STEAM CHESS ENGINE

##DESCRIPTION

A chess engine called **STEAM CHESS ENGINE** (named after the Steamledge). It is a basic Chess with an AI written in Python 3 (using python 3.7.7 and pygame 1.9.6).  The chess engine is made up of three files `main.py`, `engine.py` and `ai.py`. it takes the logic of a the **bullet chess** which changes turn from light to dark or vise-versa  if move not made after 10 seconds.

###Features

*	User interactive GUI using pygame
*	It has a Display resolution of 600 x600, sounds for both move and capture and square highlighting.
*	Built around the simple Minimax algorithm.
*	Alpha-beta pruning for improving best move searching speed
*	Move ordering based off heuristics like captures and promotions
*	Simplified Evaluation Function for board evaluation with piece-square tables and piece values
*	Uses standard Python collections and data structures for clarity and efficiency.

###Game Modes

*	Player Vs Player
*	AI Vs AI

#CODE DESCRIPTION

The codes for this chess engine is made up of three files which each having Class and functions used to produce this functional engine. The `main.py` file is the GUI of the engine use pygame to display the chess board and pieces as well as the game simulation. The `engine.py` is the engine of the chess. It consists of all the technical capability of a chess game. While the `ai.py` is the code for the AI bot below is a detail description of each file

##main.py (GUI of the Game)

This is the GUI displaying all aspects of the chess game and handling user inputs. it contains the `main()` function which display the chess game using pygame with the help of supporting functions which includes:
*	`display_game_state` :display all graphics
*	`def display_board`: display chess squares on board
*	`display_pieces`:  display chess pieces on board from current game state
*	`display_ranks_files` :display ranks (numbers) and files (letters) around board
*	`def play_sound`: plays move and captured sounds
*	`animate`: creates moving animation for chess pieces:

##engine.py (Heart of the Chess Engine)

This is the main chess game engine that implements the rules of the game and stores the state of the chess board, including its pieces and moves. This file is made of two Classes `Game_state` and `Move`. Each Class has a specific function in the engine

###Game_state

* `self.board`: 8 X 8 dimensional array (Matrix of 8 rows and 8 columns ) i.e a list of lists. Each element of the Matrix  is a string of two characters representing the chess pieces in the order "type" + "colour".. light pawn = “pl” dark pawn = “pd” and empty square = "  " double empty space.
*	`get_pawn_moves`, `get_rook_moves`, `get_knight_moves`, `get_queen_moves`, `get_king_moves` and `get_bishop_moves` : this functions Calculates all possible moves for a given color (light or dark) and appends them to a list. This includes all types of chess moves, capture, castling and enpassant
*	`make_move`: moves pieces on the board from one square to another
*	`undo_move`: this undo moves made in the by using the move_log that saves all moves done
*	`get_all_possible_moves`: this gives naive possible moves of pieces on the board without taking checks into account
*	`get_valid_moves`: gives the valid piece moves on the board while considering potential checks

###Move:

A Move class abstracting all parameters needed for moving chess pieces on the board
*	`self.start_row`: row location of piece to be moved
*	`self.start_col`: column location of piece to be moved
*	`self.end_row`: intended row destination of piece to be moved
*	`self.end_col`: intended column destination of piece to be moved
*	`self.piece_moved`: actual piece moved
*	`self.piece_captured`: opponent piece if any on the destination square

##ai.py (AI Bots)

Included in the `ai.py` is the Minimax functions, which utilizes the MiniMax algorithm to evaluate board states. The MiniMax algorithm provided comes with alpha-beta pruning, move ordering. Some of the functions used include:

*	`Evaluation`: this function evaluates the board at a given game state. It sums up the pieces on the board using piece values and also adds piece-square tables, which alter the value of a piece depending on which square it sits on.
*	`Minimax`: Minimax is a search algorithm that finds the next optimal move by minimizing the potential loss in a worst case scenario. This algorithm was adapted from Sebastian Lague’s Algorithms Explained – minimax and alpha-beta pruning. It uses the evaluation function to determine the best possible move to win the game. The Minimax was made better using the alpha beta pruning, This significantly reduces the number of moves required to be generated hence increasing search speed without affecting the outcome
*	`Move_ordering`: this function helps the ai to order moves base on importance (capture, promotion, defending the king) this helps to further assist in choosing the best move without making unnecessary sacrifices.
*	`light_pieces and dark_pieces`: This are dictionaries containing all the pieces at a particular game state which will assist in making faster static evaluation of the game state by the evaluation function.  It is updated as moves and captures are being made
*	`update_pieces_dictionaries`: This updates light_pieces and dark_pieces during the hidden simulation in the minimax algorithm. It creates a copy of the dictionary to be used by the minimax during tree search for best move.
*	`ai_light_move` and `ai_dark_move`: this serves as a plug for the ai  to make moves generated using the minimax algorithm on the board. It also updates the light_pieces and dark_pieces dictionary
*	`ai_move`: determines the turn for both team's AI also saves a running memory of the board state with moves and captures
*	`ai_reset`: resets the light pieces and dark pieces dictionaries when AI mode is activated/deactivated (in case moves were made outside AI mode)

##HOW TO PLAY

###Installation:

*	Download and extract repo in a folder on your system
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
*	Start game by run the following command:
- __Linux__ or __Mac__:
```
py main.py
```
- __Windows__:
````
python main.py
````

##USER INPUTS

By the default the game is Player Vs Player
*	Press “A” on keyboard to activate or deactivate AI mode
*	Press “R” on keyboard to reset game
*	Press “U” on keyboard to undo move made
*	Mouse left click on piece and square to select piece and make move respectively
*	Input “Q”, “R” , “B” or “K” to prompt pawn promotions

##LIMITATION:

*	The AI sometimes finds it hard to make checkmate at end game. This can be corrected if a separate piece-square tables are used for end games
*	Depth for the minimax does not exceed 3… it takes too long to search (above expected 10 seconds)
*	No provision for player Vs AI
