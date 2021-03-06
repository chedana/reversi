"""
An AI player for Othello. 
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

cache = {}
def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)

# Method to compute utility value of terminal state
def compute_utility(board, color):
    #IMPLEMENT
    score1 , score2 = get_score(board)
    if color == 1:
        return score1 - score2
    else:
        return score2-score1

# Better heuristic value of board
def compute_heuristic(board, color): #not implemented, optional
    #IMPLEMENT
    return 0 #change this!

############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching = 0):
    global cache
    current = color, board
    if caching == 1 and current in cache:
        return cache[current]
    #IMPLEMENT
    if limit == 0:
        return None,compute_utility(board,color)
    minVal = float("inf")
    move = None
    anti_color = 3-color
    moves = get_possible_moves(board,anti_color)
    if not moves:
        if caching == 1:
            cache[current] = None,compute_utility(board,color)
        return None, compute_utility(board,color)

    for i,j in moves:
        new_board = play_move(board,anti_color,i,j)
        t_move , score = minimax_max_node(new_board,color,limit-1,caching)
        if score < minVal:
            minVal = score
            move = (i,j)
    if caching == 1:
        cache[current] = (move,minVal)
    return (move,minVal)

def minimax_max_node(board, color, limit, caching = 0): #returns highest possible utility
    global cache
    current = color, board
    if caching == 1 and current in cache:
        return cache[current]
    if limit == 0:
        return None,compute_utility(board,color)
    maxVal = float("-inf")
    move = None
    moves = get_possible_moves(board,color)
    if not moves:
        if caching == 1:
            cache[current] = None,compute_utility(board,color)
        return None,compute_utility(board,color)
    for i,j in moves:
        new_board = play_move(board,color,i,j)
        t_move,score = minimax_min_node(new_board,color,limit-1,caching)
        if score > maxVal:
            maxVal = score
            move = (i,j)
    if caching == 1:
        cache[current] = (move,maxVal)
    return (move,maxVal)

def select_move_minimax(board, color, limit, caching = 0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    """
    #IMPLEMENT
    move , utility = minimax_max_node(board,color,limit,caching)

    return move #change this!

############ ALPHA-BETA PRUNING #####################
def node_ordering_heuristic(board,moves,color,anti_color,ordering,reverse):
    return sorted(moves, key = lambda x: compute_utility(play_move(board,color,x[0],x[1]),anti_color),reverse = reverse)



def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    global cache
    current = color, board
    if caching == 1 and current in cache:
        return cache[current]
    if limit == 0:
        return None,compute_utility(board,color)
    anti_color = 3 - color
    moves = None
    if ordering:
        moves = node_ordering_heuristic(board, get_possible_moves(board, anti_color), anti_color, color, ordering, False)
    else:
        moves = get_possible_moves(board, anti_color)
    if not moves:
        if caching == 1:
            cache[current] = None, compute_utility(board, color)
        return None, compute_utility(board, color)
    minVal = float('inf')
    move = None
    for i,j in moves:
        new_board = play_move(board, anti_color, i, j)
        t_move, score = alphabeta_max_node(new_board, color, alpha, beta, limit - 1, caching)
        if score < minVal:
            minVal = score
            move = (i,j)
        if beta > minVal:
            beta = minVal
            if beta <= alpha:
                break
    if caching == 1:
        cache[current] = move, minVal
    return move, minVal

def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    global cache
    current = color, board
    if caching == 1 and current in cache:
        return cache[current]
    if limit == 0:
        return None,compute_utility(board,color)
    moves = None
    if ordering:
        moves = node_ordering_heuristic(board, get_possible_moves(board, color), color, color, ordering, True)
    else:
        moves = get_possible_moves(board, color)
    if not moves:
        if caching == 1:
            cache[current] = None, compute_utility(board, color)
        return None, compute_utility(board, color)
    maxVal = float('-inf')
    move = None
    for i,j in moves:
        new_board = play_move(board, color, i, j)
        t_move, score = alphabeta_min_node(new_board, color, alpha, beta, limit - 1, caching)
        if  score > maxVal:
            maxVal = score
            move = (i,j)
        if alpha < maxVal:
            alpha = maxVal
            if beta <= alpha:
                break
    if caching == 1:
        cache[current] = move, maxVal
    return move, maxVal

def select_move_alphabeta(board, color, limit, caching = 0, ordering = 0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations.
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations.
    """
    #IMPLEMENT
    alpha = float('-inf')
    beta = float('inf')
    move, utility = alphabeta_max_node(board, color, alpha, beta, limit, caching, ordering)
    return move

####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Othello AI") # First line is the name of this AI
    arguments = input().split(",")
    
    color = int(arguments[0]) #Player color: 1 for dark (goes first), 2 for light. 
    limit = int(arguments[1]) #Depth limit
    minimax = int(arguments[2]) #Minimax or alpha beta
    caching = int(arguments[3]) #Caching 
    ordering = int(arguments[4]) #Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): #run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: #else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)
            
            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()
