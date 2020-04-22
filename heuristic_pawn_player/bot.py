import random

DEBUG = 1
def dlog(str):
    if DEBUG > 0: log(str)

board_size = get_board_size()
team = get_team()
opp_team = Team.WHITE if team == Team.BLACK else Team.BLACK
robottype = get_type()
if team == Team.WHITE:
    forward = 1
    index = 0
else:
    forward = -1
    index = board_size - 1
roundNum = 0 # round number local to the unit

def get(r, c):
    # check space, except doesn't hit you with game errors
    if r < 0 or c < 0 or c >= board_size or r >= board_size:
        return False
    if r < row-2 or r > row+2 or c < col-2 or c > col+2:
        return False
    return board[r][c]
def can_move_forward():
    if forward > 0 and row == board_size-1:
        return False
    if forward < 0 and row == 0:
        return False
    if board[row+forward][col]:
        return False
    return True

def max(a, b):
    return a if a > b else b
def min(a, b):
    return a if a < b else b
def sum(l):
    out = 0
    for elt in l:
        out += elt
    return out

def pawn_get_board():
    board = [[False]*board_size for r in range(board_size)]
    for r, c, bot in sense():
        board[r][c] = bot
    return board

def get_defending_count():
    count = 0
    for d in [-1, 1]:
        if get(row+forward, col+d) == team and get(row+2*forward, col+2*d) == opp_team:
            count += 1
    return count
def get_forward_danger():
    danger, defense = 0, 0
    for d in [-1, 1]:
        if get(row, col+d) == team: defense += 1
        if get(row+2*forward, col+d) == opp_team: danger += 1
    return danger, defense

FORWARD_CHANCE_1 = 8e-2
FORWARD_CHANCE_2 = 3e-2
def pawn_turn():
    board = pawn_get_board()
    for d in [-1, 1]:
        if get(row+forward, col+d) == opp_team:
            capture(row+forward, col+d)
            return
    if not can_move_forward(): return
    # defending_count = get_defending_count()
    # if defending_count > 0: return # keep supporting our troops
    forward_danger, forward_defense = get_forward_danger()
    if forward_danger <= 0:
        move_forward()
        return
    if forward_defense < 2:
        return
    if forward_danger == 1:
        if random.random() < FORWARD_CHANCE_1:
            move_forward()
        return
    if forward_danger == 2:
        if random.random() < FORWARD_CHANCE_2:
            move_forward()
        return
    dlog('WARNING: Reached the unreachable star')

def pawn_turn_wrapper():
    global row, col, board, roundNum
    row, col = get_location()
    board = pawn_get_board()
    pawn_turn()
    roundNum += 1
    bytecode = get_bytecode()
    dlog('Done! Bytecode left: ' + str(bytecode))

UNIFORM_MIX = 0.01
def overlord_turn():
    board = get_board()
    weights = [0]*board_size
    for r,row in enumerate(board):
        for c,value in enumerate(row):
            if value == opp_team:
                weight = 1
                if abs(r - index) < 6:
                    weight *= 25
                weights[c] = weights[c] + weight/2
                if c-1 >= 0: weights[c-1] = weights[c-1] + weight
                if c+1 < board_size: weights[c+1] = weights[c+1] + weight
            elif value == team:
                weights[c] = weights[c] - 1
    
    weights = [max(0, w)+UNIFORM_MIX for w in weights]
    for c in range(board_size):
        if check_space(index, c):
            weights[c] = 0
    total_weight = sum(weights)
    i = random.random() * total_weight
    accum = 0
    for c,weight in enumerate(weights):
        if accum + weight > i:
            return spawn(index,c)
        accum += weight

def overlord_turn_wrapper():
    global roundNum
    overlord_turn()
    roundNum += 1
    bytecode = get_bytecode()
    dlog('Done! Bytecode left: ' + str(bytecode))    

if robottype == RobotType.PAWN:
    turn = pawn_turn_wrapper
else:
    turn = overlord_turn_wrapper
