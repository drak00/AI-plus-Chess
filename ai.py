import pygame
import random
from engine import Game_state, Move
from copy import deepcopy
from math import inf
gs =Game_state()

piece_values = {
            'p': 10,
            'n': 30,
            'b': 30,
            'r': 50,
            'q': 90,
            'k': 900
		}   # weight for  each piece in the game

def get_light_score(board):
    """
        Calculates the total score of light on the Board

        input parameter(s):
        board
        return parameter(s):
        score
    """
    light_score = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j][1] == "l":
                light_score += piece_values[board[i][j][0]]  # add weigth of piece to score if found
    return light_score
def get_dark_score(board):
    """
        Calculates the total score of light on the Board

        input parameter(s):
        board
        return parameter(s):
        score
    """
    dark_score = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j][1] == "d":
                dark_score += piece_values[board[i][j][0]]  # add weigth of piece to score if found
    return dark_score

def eval_board(board, maximizing_player):
    """
        evaluates current board state for each player

        input parameter(s):
        board ----> game Board
        maximizing_player -----> boolean
        return parameter(s):
        evaluation
    """
    if maximizing_player:
        eval = get_light_score(board) - get_dark_score(board)
    else:
        eval = get_dark_score(board) - get_light_score(board)
    return eval

def minimax(board, depth, maximizing_player):
    """
        minimax algorithm to get best move for each turn

        input parameter(s):
        board -----> game board
        depth ----> how deep should it go (int)
        return parameter(s):
        best moved
        evaluation
    """
    if depth == 0:
        return None, eval_board(board, maximizing_player) #return evaluation when depth is 0
    moves = get_moves()   #geting moves
    best_move = random.choice(moves)  #setting best_move to a random move
    if maximizing_player:
        max_eval = -inf # setting to negative infinity
        alpha = -inf # setting to negative infinity...... to be used for pruning
        beta = inf # setting to positive negative infinity...... to be used for pruning
        for move in moves:
            print(move)
            gs.make_move(move, True) # making move to evaluate board
            current_eval = minimax(board, depth-1, False)[1] # evaluation by decrease depth it it reaches node
            print(current_eval)
            gs.undo_move(True)  #undo move simulation
            if current_eval < max_eval:
                best_move = move
            alpha = min(alpha, current_eval)
            if beta >= alpha:
                break
        return best_move, max_eval
    else:
        min_eval = inf
        beta = inf # setting to positive negative infinity...... to be used for pruning
        alpha = -inf # setting to negative infinity...... to be used for pruning
        for move in moves:
            print(move)
            gs.make_move(move, True)
            current_eval = minimax(board, depth-1, True)[1] # evaluation by decrease depth it it reaches node
            gs.undo_move(True) #undo move simulation
            if current_eval > min_eval:
                best_move = move
            beta = max(beta, current_eval)
            if beta >= alpha:
                break
        return best_move, min_eval

def get_moves():
    """
        get all moves for all pieces

        input parameter(s):
        board
        return parameter(s):
        moves
    """
    moves =[]
    for r in range(len(gs.board)):
        for c in range(len(gs.board[r])):
            piece = gs.board[r][c][0]
            if piece == "p":
                gs.get_pawn_moves(r, c, moves)
            elif piece == gs.board[r][c][0]=="r":
                gs.get_rook_moves(r, c, moves)
            elif piece == gs.board[r][c][0]=="b":
                gs.get_bishop_moves(r, c, moves)
            elif piece == gs.board[r][c][0]=="q":
                gs.get_queen_moves(r, c, moves)
            elif piece == gs.board[r][c][0]=="k":
                gs.get_king_moves(r, c, moves)
            elif piece == gs.board[r][c][0]=="n":
                gs.get_knight_moves(r, c, moves)
    return moves

#y = eval_board(gs.board, gs.light_to_move)
#a = get_light_score(gs.board)
#b = get_moves(gs.board)
x = minimax(gs.board, 2, gs.light_to_move)
#print(a, b, y
print(x)
