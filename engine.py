## This is the main chess game engine that implements the rules of the game
## and stores the state of the the chess board, including its pieces and moves


class Game_state():
	
    def __init__(self):
        """
            The chess board is an 8 X 8 dimensional array (Matrix of 8 rows and 8 columns )
            i.e a list of lists. Each element of the Matrix is a string of two characters
            representing the chess pieces in the order "type" + "colour"

			light pawn = pl
			dark pawn  = pd

			light knight = nl
			dark knight  = nd
			e.t.c

			empty board square = "  " ---> double empty space

		"""

        self.board = [

			["rd", "nd", "bd", "qd", "kd", "bd", "nd", "rd"],
			["pd", "pd", "pd", "pd", "pd", "pd", "pd", "pd"],
			["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
			["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
			["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
			["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
			["pl", "pl", "pl", "pl", "pl", "pl", "pl", "pl"],
			["rl", "nl", "bl", "ql", "kl", "bl", "nl", "rl"]]

        self.light_to_move = True # True = light's turn to play; False = dark's turn to play
        self.move_log = []        # keeps a log of all moves made withing a game
        self.move_piece = {"p":self.get_pawn_moves, "r":self.get_rook_moves, \
                        "q":self.get_queen_moves, "k":self.get_king_moves, \
                        "b":self.get_bishop_moves, "n":self.get_knight_moves}
        self.king_pos = {"kl":(7,4), "kd":(0,4)} # light king and Dark King starting row and column
        self.check_mate = False # setting checkmate false
        self.stale_mate = False #setting


    def get_pawn_moves(self, r, c, moves):
        """
            Calculates all possible pawn moves for a given color (light or dark)
            and appends them to a list

            input parameter(s):
            r     --> starting row (int)
            c     --> starting colum (int)
            moves --> possible moves container (list)

            return parameter(s):
            None
        """
        
        ## FIX
        if self.light_to_move: # if it's light's turn to move
            
            # if square is empty and in front of pawn
            if (r-1 >= 0) and (self.board[r-1][c] == "  "):
                moves.append(Move((r, c), (r-1, c), self.board)) # create a move object and append to list
                # if square two steps in front of pawn is empty and it is the pawn's first move
                if (r == 6) and (self.board[r-2][c] == "  "):
                    moves.append(Move((r, c), (r-2, c), self.board)) # create a move object and append to list
            
            
            # if square on pawn's left diagonal has an opponent piece
            if ((r-1 >= 0) and (c-1 >= 0)) and (self.board[r-1][c-1][1] == "d"):
                moves.append(Move((r, c), (r-1, c-1), self.board)) # create a move object and append to list
            
            # if square on pawn's right diagonal has an opponent piece
            if ((r-1 >= 0) and (c+1 < len(self.board))) and (self.board[r-1][c+1][1] == "d"):
                moves.append(Move((r, c), (r-1, c+1), self.board)) # create a move object and append to list

            # en-passant move
            if len(self.move_log) != 0: # if move log is not empty
                if self.move_log[-1].piece_moved[0] == 'p': # if last piece moved is a pawn
                    # if the pawn made a double move
                    if (self.move_log[-1].start_row == 1) and (self.move_log[-1].end_row == 3):
                        # if the pawn made a double move on this piece's left side 
                        if (self.move_log[-1].end_row, self.move_log[-1].end_col) == (r,c-1):
                            # create a move object and append to list
                            moves.append(Move((r, c), (r-1, c-1), self.board, move_type="en_passant"))
                        # if the pawn made a double move on this piece's right side 
                        elif (self.move_log[-1].end_row, self.move_log[-1].end_col) == (r,c+1):
                            # create a move object and append to list
                            moves.append(Move((r, c), (r-1, c+1), self.board, move_type="en_passant"))
                        # if the pawn did not make a move on this pawn's side
                        else:
                            pass
			

        else: # if it's dark's turn to move
            
            # if square is empty and in front of pawn
            if (r+1 < len(self.board)) and (self.board[r+1][c] == "  "):
                moves.append(Move((r, c), (r+1, c), self.board)) # create a move object and append to list
                # if square two steps in front of pawn is empty and it is the pawn's first move
                if (r == 1) and (self.board[r+2][c] == "  "):
                    moves.append(Move((r, c), (r+2, c), self.board)) # create a move object and append to list
            
            # if square on pawn's left diagonal has an opponent piece
            if ((r+1 < len(self.board)) and (c-1 >= 0)) and (self.board[r+1][c-1][1] == "l"):
                moves.append(Move((r, c), (r+1, c-1), self.board)) # create a move object and append to list
            
            # if square on pawn's right diagonal has an opponent piece
            if ((r+1 < len(self.board)) and (c+1 < len(self.board))) and (self.board[r+1][c+1][1] == "l"):
                moves.append(Move((r, c), (r+1, c+1), self.board)) # create a move object and append to list
            
            # en-passant move
            if len(self.move_log) != 0: # if move log is not empty
                if self.move_log[-1].piece_moved[0] == 'p': # if last piece moved is a pawn
                    # if the pawn made a double move
                    if (self.move_log[-1].start_row == 6) and (self.move_log[-1].end_row == 4):
                        # if the pawn made a double move on this piece's left side 
                        if (self.move_log[-1].end_row, self.move_log[-1].end_col) == (r,c+1):
                            # create a move object and append to list
                            moves.append(Move((r, c), (r+1, c+1), self.board, move_type="en_passant"))
                        # if the pawn made a double move on this piece's right side 
                        elif (self.move_log[-1].end_row, self.move_log[-1].end_col) == (r,c-1):
                            # create a move object and append to list
                            moves.append(Move((r, c), (r+1, c-1), self.board, move_type="en_passant"))
                        # if the pawn did not make a move on this pawn's side
                        else:
                            pass


    def get_bishop_moves(self, r, c, moves):
        
        """
            calculates all possible bishop moves for a given colour (light or dark)
            and appends them to a list

            input parameters:
            r     --> starting row (int)
            c     --> starting column (int)
            moves --> posiible moves container (list)

            return parameter(s):
            None
        """
        direction = ((-1, -1), (1, 1), (1, -1), (-1, 1))  # possible  Bishop direction
        if self.light_to_move:  # light piece turn to move
            for d in direction:
                for i in range(1, len(self.board)):
                    rownum = r + d[0] * i
                    colnum = c + d[1] * i
                    if (0 <= rownum < len(self.board)) and (
                            0 <= colnum < len(self.board)):  # making sure r and c on board
                        if self.board[rownum][colnum] == "  ":  # if square is empty
                            moves.append(Move((r, c), (rownum, colnum), (self.board)))
                        elif self.board[rownum][colnum][1] == "d":  # if square has opponent piece
                            moves.append(Move((r, c), (rownum, colnum), (self.board)))
                            break
                        else:
                            break  # when ally piece encountered
                    else:
                        break  # when off the board
        else:  # Dark piece turn to move
            for d in direction:
                for i in range(1, len(self.board)):
                    rownum = r + d[0] * i
                    colnum = c + d[1] * i
                    if (0 <= rownum < len(self.board)) and (
                            0 <= colnum < len(self.board)):  # making sure r and c on board
                        if self.board[rownum][colnum] == "  ":  # if square is empty
                            moves.append(Move((r, c), (rownum, colnum), (self.board)))
                        elif self.board[rownum][colnum][1] == "l":  # if square has opponent piece
                            moves.append(Move((r, c), (rownum, colnum), (self.board)))
                            break
                        else:
                            break  # when ally piece encountered
                    else:
                        break  # when off the board


    def get_knight_moves(self, r, c, moves):

        """
            calculates all possible knight moves for a given colour (light or dark)
            and appends them to a list

            input parameters:
            r     --> starting row (int)
            c     --> starting column (int)
            moves --> posiible moves container (list)

            return parameter(s):
            None
        """
        #possible squares for knight move
        squares = (
            (r+2,c+1), (r+2,c-1), (r-2,c+1), (r-2,c-1),
            (r+1,c+2), (r+1,c-2), (r-1,c+2), (r-1,c-2)
        )

        if self.light_to_move: # if it's light's turn to move
            available_squares = (" ", "d") #squares the knight can move to

            for square in squares:
                i,j = square
                if ( (0 <= i < len(self.board)) and (0 <= j < len(self.board))
                    and (self.board[i][j][1] in available_squares) ):

                    moves.append(Move((r, c), square, self.board)) # create a move object and append to list
        

        else: #if it's dark's turn to move
            available_squares = (" ", "l") #squares the knight can move to

            for square in squares:
                i,j = square
                if ( (0 <= i < len(self.board)) and (0 <= j < len(self.board))
                    and (self.board[i][j][1] in available_squares) ):

                    moves.append(Move((r, c), square, self.board)) # create a move object and append to list


    def get_king_moves(self, r, c, moves):
        """
            calculates all possible king moves for a given colour (light or dark)
            and appends them to a list

            input parameters:
            r     --> starting row (int)
            c     --> starting column (int)
            moves --> posiible moves container (list)

            return parameter(s):
            None
        """

        directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        enemy_color = "d" if self.light_to_move else "l"

        for d in directions:
            end_row = r + d[0]
            end_col = c + d[1]

            if 0 <= end_row < 8 and 0<= end_col < 8:
                destination = self.board[end_row][end_col]
                if destination[1] == enemy_color or destination == "  ":
                    moves.append(Move((r, c), (end_row, end_col), self.board))

            

    def get_rook_moves(self, r, c, moves):
        """
            calculates all possible rook moves for a given colour (light or dark)
            and appends them to a list

            input parameters:
            r     --> starting row (int)
            c     --> starting column (int)
            moves --> posiible moves container (list)

            return parameter(s):
            None
         """
        direction = (-1, 1) # possible direction

        if self.light_to_move: # if it's light's turn to move

            for d in direction:
                #rows
                for i in range(1,len(self.board)):
                    rownum = r + d*i
                    if (0 <= rownum < len(self.board)): # making sure row is on board
                        if self.board[rownum][c] == "  ": # if square is empty
                            moves.append(Move((r,c), (rownum,c), (self.board)))
                        elif self.board[rownum][c][1] == "d": # if square has opponent piece
                            moves.append(Move((r,c), (rownum,c), (self.board)))
                            break
                        else:
                            break # when ally piece encountered
                    else:
                        break # when off the board
                #columns
                for i in range(1,len(self.board)):
                    colnum = c + d*i
                    if (0 <= colnum < len(self.board)): # making sure column is on board
                        if self.board[r][colnum] == "  ": # if square is empty
                            moves.append(Move((r,c), (r,colnum), (self.board)))
                        elif self.board[r][colnum][1] == "d": # if square has opponent piece
                            moves.append(Move((r,c), (r,colnum), (self.board)))
                            break
                        else:
                            break # when ally piece encountered
                    else:
                        break # when off the board

         #if it's dark's turn to move
        else:
            for d in direction:
                #rows
                for i in range(1,len(self.board)):
                    rownum = r + d*i
                    if (0 <= rownum < len(self.board)): # making sure row is on board
                        if self.board[rownum][c] == "  ": # if square is empty
                            moves.append(Move((r,c), (rownum,c), (self.board)))
                        elif self.board[rownum][c][1] == "l": # if square has opponent piece
                            moves.append(Move((r,c), (rownum,c), (self.board)))
                            break
                        else:
                            break # when ally piece encountered
                    else:
                        break # when off the board
                #columns
                for i in range(1,len(self.board)):
                    colnum = c + d*i
                    if (0 <= colnum < len(self.board)): # making sure column is on board
                        if self.board[r][colnum] == "  ": # if square is empty
                            moves.append(Move((r,c), (r,colnum), (self.board)))
                        elif self.board[r][colnum][1] == "l": # if square has opponent piece
                            moves.append(Move((r,c), (r,colnum), (self.board)))
                            break
                        else:
                            break # when ally piece encountered
                    else:
                        break # when off the board


    def get_queen_moves(self, r, c, moves):
        """
        Calculates all possible queen moves for a given color (light or dark)
        based on bishop and rook moves.

        input parameter(s):
        r     --> starting row (int)
        c     --> starting colum (int)
        moves --> possible moves container (list)

        return parameter(s):
        None
        """
        ##TODO
        self.get_bishop_moves(r, c, moves)
        self.get_rook_moves(r, c, moves)


    def make_move(self, move):
        """
            moves pieces on the board
        """
        if move.move_type == "en_passant": # if move is an en-passant move
            if self.light_to_move: # if it's light's turn to move
                # capturing piece
                move.piece_captured = self.board[move.end_row + 1][move.end_col]
                self.board[move.end_row + 1][move.end_col] = "  "
            else: # if it's dark's turn to move
                # capturing piece
                move.piece_captured = self.board[move.end_row - 1][move.end_col]
                self.board[move.end_row - 1][move.end_col] = "  "
        
        self.board[move.start_row][move.start_col] = "  "
        self.board[move.end_row][move.end_col] = move.piece_moved
        
        #Updating king position
        if move.piece_moved[0] == "k": # king piece moved
            self.king_pos[move.piece_moved] = (move.end_row, move.end_col) # update tuple containing postion

        self.move_log.append(move) # log move
        self.light_to_move = not self.light_to_move # next player to move


    def undo_move(self, look_ahead_mode = False):
        """
            undoes last move
        """
        if self.move_log:
            last_move = self.move_log.pop()
            self.board[last_move.start_row][last_move.start_col] = last_move.piece_moved
            
            if last_move.move_type == "en_passant": # if the last move was an en-passant move
                
                if not self.light_to_move: # if the last move was light's move
                    # undo piece capture
                    self.board[last_move.end_row + 1][last_move.end_col] = last_move.piece_captured
                else: # if the last move was dark's move
                    # undo piece capture
                    self.board[last_move.end_row - 1][last_move.end_col] = last_move.piece_captured

                # remove piece from occupied square
                self.board[last_move.end_row][last_move.end_col] = "  "

            else: # if the last move was not an en-passant move
                # undo piece capture
                self.board[last_move.end_row][last_move.end_col] = last_move.piece_captured
                
                #Undoing kings movement
                if last_move.piece_moved[0] == "k": #   king piece moved undo
                    self.king_pos[last_move.piece_moved] = (last_move.start_row, last_move.start_col) # update tuple by undoing move

            self.light_to_move = not self.light_to_move

            self.undo_text = "undoing -> {}".format(last_move.get_chess_notation()) # an undoing statement to be printed to show undo done
        else:
            print("All undone!")


    def get_valid_moves(self):
        """
            this function updates the get_possible_moves to valid chess valid_moves
            it identifies if the king is in check and provides solution to avoid checkmate
            it calls the get_possible_moves function and incheck function

            input parameters:
            none

            return parameter(s):
            moves
        """
        # passing in two varibles moves and turns because it returns 2
        moves, turn = self.get_possible_moves()
        # iterating the index of the moves from the last to 1st because we will
        #be removing moves which will skip moves if iterated from 1st to last
        for i in range(len(moves)-1,-1,-1):
            #making a move to check if it will lead to the king being attacked
            self.make_move(moves[i])
            self.light_to_move = not  self.light_to_move # switching turn to opponent
            if self.in_check():  # checking if opposition move attack king
                moves.remove(moves[i]) # remove moves leading to king being attacked
            self.light_to_move  = not self.light_to_move #switching back
            self.undo_move() # undo the move done... because this are hidden testing moves

        if len(moves) == 0 and self.in_check(): # checking if there are no posssible valid moves  and king incheck
            self.check_mate = True # check mate
        elif len(moves) == 0: # checking if there are no possible moves but king not incheck
            self.stale_mate = True # stalemate
        else:
            self.check_mate = False
            self.stale_mate = False

        return moves, turn

    def get_possible_moves(self):

        moves = []

        turn = "l" if self.light_to_move else "d"

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j][1] == turn:
                    self.move_piece[self.board[i][j][0]](i, j, moves)

        return moves, turn
      
      
    def in_check(self):
        """
          uses the square_under_attack fuction to test the moves that will lead to king being attacked
          checks for both light and dark pieces

          input parameter(s):
          None

          return parameter(s):
          Boolean

        """
        if self.light_to_move: # lights turn to move
          # checks light king under attack in respact to its position
          return self.square_under_attack(self.king_pos["kl"][0],self.king_pos["kl"][1])
        else:
          # checks light king under attack in respect to its position
          return self.square_under_attack(self.king_pos["kd"][0],self.king_pos["kd"][1])


    def square_under_attack(self, r,c):
        """
          uses the kings postion on the board to determine if its under attacked

          input parameter(s):
          r -----> row of the piece position (int)
          c -----> column of the piece position (int)

          return parameter(s):
          Boolean
        """
        self.light_to_move = not self.light_to_move # switching turns to opponent to get the opponent moves
        oppostion_moves, turn= self.get_possible_moves() # passing in two varibles moves and turns because it returns 2
        self.light_to_move = not self.light_to_move # change back the turn to check if opposition move attack king
        for move in oppostion_moves: # iterating through opposition moves
          if (move.end_row == r) and (move.end_col == c): # checking to see if the move is same position as that of the king
            return True # true if same position
        return False # false if not same position as king


 
class Move():

    # map ranks to rows
    ranks_to_rows = {"1":7, "2":6, "3":5, "4":4,
                    "5":3, "6":2, "7":1, "8":0}

    # map rows to ranks (revers of ranks to rows)
    rows_to_ranks = {row:rank for rank, row in ranks_to_rows.items()}

    # map files to columns
    files_to_cols = {"a":0, "b":1, "c":2, "d":3,
                    "e":4, "f":5, "g":6, "h":7}

    # map columns to files (revers of files to columns)
    cols_to_files = {col:file for file, col in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board, move_type="normal"):
        """
            A Move class abstracting all parameters needed
            for moving chess pieces on the board

            input parameter(s):
            start_sq --> (row, column) of piece to be moved (tuple)
            end_square --> (row, column) of move destination on the board (tuple)
            board --> board object referencing current state of the board (class Game_state)
        """
        self.start_row = start_sq[0] # row location of piece to be moved
        self.start_col = start_sq[1] # column location of piece to be moved
        self.end_row = end_sq[0] # intended row destination of piece to be moved
        self.end_col = end_sq[1] # intended column destiantion of piece to e moved
        self.piece_moved = board[self.start_row][self.start_col] # actual piece moved
        self.piece_captured = board[self.end_row][self.end_col] # opponent piece if any on the destination square
        self.move_type = move_type # variable to store move type

    def get_chess_notation(self):
        """
            creates a live commentary of pieces moved on the chess board during a game

            input parameter(s):
            None

            return parameter(s)
            commentary (string)
        """
        return self.piece_moved[0].upper() + "(" + self.get_rank_file(self.start_row, self.start_col) + ") to " + self.get_rank_file(self.end_row, self.end_col) + \
            "(" + self.piece_captured[0].upper() + " captured!)" if self.piece_captured != "  " else self.piece_moved[0].upper() + "(" + self.get_rank_file(self.start_row, self.start_col) + ") to " + \
            self.get_rank_file(self.end_row, self.end_col)


    def get_rank_file(self, r, c):
        """
            calls cols_to_file and rows_to_rank attributes

            input parameter(s):
            r --> row to be converted to rank (int)
            c --> column to be converted to file (int)

            return parameter(s):
            "file" + "rank" (str)
        """
        return self.cols_to_files[c] + self.rows_to_ranks[r]


    def __eq__(self, other):
        """
            operator overloading for equating two move objects
        """

        if isinstance(other, Move): # if first (self) and second (other) parameters are both Move objects
            return self.start_row == other.start_row and self.start_col == other.start_col and \
                    self.end_row == other.end_row and self.end_col == other.end_col and \
                    self.move_type == other.move_type
        else:
            return False


    def __ne__(self, other):
        """
            "not equals to" --> conventional counterpart to __eq__
        """
        return self.__eq__(other)


    def __str__(self):
        """
            operator overloading for printing Move objects
        """
        return "({}, {}) ({}, {})".format(self.start_row, self.start_col, self.end_row, self.end_col)


