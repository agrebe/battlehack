import random

DEBUG = 1
def dlog(str):
    if DEBUG > 0: log(str)

board_size = get_board_size()
team = get_team()
opp_team = Team.WHITE if team == Team.BLACK else Team.BLACK
robottype = get_type()
if robottype == RobotType.PAWN:
    row, col = get_location()
if team == Team.WHITE:
    forward = 1
    index = 0
else:
    forward = -1
    index = board_size - 1
roundNum = 0 # round number local to the unit
eps = 1e-1 # probability to advance with two defenders (on sides)
delta = 20e-2 # probability for columns 1 and 14 to advance with one defender

def check_space_wrapper(r, c):
    # check space, except doesn't hit you with game errors
    if r < 0 or c < 0 or c >= board_size or r >= board_size:
        return False
    if r < row-2 or r > row+2 or c < col-2 or c > col+2:
        return False
    return check_space(r, c)
def capture_wrapper(r, c):
    global row, col
    capture(r, c)
    row = r
    col = c
def move_forward_wrapper():
    global row
    move_forward()
    row += forward
def can_move_forward(board):
    if forward > 0 and row == board_size-1:
        return False
    if forward < 0 and row == 0:
        return False
    if board[row+forward][col]:
        return False
    return True
def try_move_forward(board):
    if can_move_forward(board):
        move_forward_wrapper()

def max(a, b):
    return a if a > b else b
def min(a, b):
    return a if a < b else b

def pawn_get_board():
    board = [[False]*board_size for r in range(board_size)]
    for r, c, bot in sense():
        board[r][c] = bot
        dlog("Sensing bot: " + str(board[r][c]))
    return board

def pawn_turn():
    global row, col
    dlog('My location is: ' + str(row) + ' ' + str(col))
    board = pawn_get_board()

    # try capturing pieces
    if check_space_wrapper(row + forward, col + 1) == opp_team: # up and right
        capture_wrapper(row + forward, col + 1)
        dlog('Captured at: (' + str(row + forward) + ', ' + str(col + 1) + ')')
        return
    if check_space_wrapper(row + forward, col - 1) == opp_team: # up and left
        capture_wrapper(row + forward, col - 1)
        dlog('Captured at: (' + str(row + forward) + ', ' + str(col - 1) + ')')
        return
    # an edge bot can advance if it has a defender
    # TODO: Maybe also make sure the defender won't move out of the way?
    if (col == 0 and team == check_space_wrapper(row, 1)) or (col == 15 and team == check_space_wrapper(row, 14)):
        try_move_forward(board)
        dlog('Moved forward thanks to defender!')
        return
    # other bots can advance if they have two defenders at least with some probability
    if (team == check_space_wrapper(row, col-1) and team == check_space_wrapper(row, col+1)) and (col <= 3 or col >= 12) and random.random() < eps:
        try_move_forward(board)
        dlog('Moved forward thanks to two defenders!')
        return
    if (col == 1) and (team == check_space_wrapper(row, col-1) or team == check_space_wrapper(row, col+1)) and random.random() < delta:
        try_move_forward(board)
        dlog('Moved forward thanks to one defender!')
        return
    # if a pawn sees a wall of pawns to its left (all 10 visible squares occupied by friendly pawns)
    # and if that pawn is on the left half of the board, then advance
    if (col == 1):
        wall = True
        for i in range(5): wall = wall and team == check_space_wrapper(row+i-2, col-1)
        if (wall):
            try_move_forward(board)
            return
 
    if (col > 1 and col < 8):
        wall = True
        for i in range(5): wall = wall and team == check_space_wrapper(row+i-2, col-1)
        for i in range(5): wall = wall and team == check_space_wrapper(row+i-2, col-2)
        if (wall):
            try_move_forward(board)
            return
    
    # if there is an enemy pawn (2,1) or (2,-1) away, don't move forward
    if (opp_team == check_space_wrapper(row + 2*forward, col+1) or opp_team == check_space_wrapper(row + 2*forward, col-1)):
        dlog('Waiting, unit ahead:' + str(board[row+2*forward][col+1]) + ' ' + str(board[row+2*forward][col-1]))
        dlog('Waiting, unit ahead:' + str(check_space_wrapper(row + 2*forward, col+1)) + ' ' + str(check_space_wrapper(row + 2*forward, col-1)))
        return

    # otherwise try to move forward
    try_move_forward(board)
    dlog('Moved forward!')

def pawn_turn_wrapper():
    pawn_turn()
    bytecode = get_bytecode()
    dlog('Done! Bytecode left: ' + str(bytecode))

def overlord_turn():
    global roundNum
    roundNum += 1
    if roundNum == 1:
        spawn(index, 1)
    elif roundNum == 2:
        spawn(index, 14)
    elif roundNum == 3:
        spawn(index, 4)
    elif roundNum == 4:
        spawn(index, 11)
    elif roundNum == 5:
        spawn(index, 7)
    elif roundNum == 6:
        spawn(index, 8)
    elif roundNum == 7:
        spawn(index, 0)
    elif roundNum == 8:
        spawn(index, 15)
    else:
        # if there is a column where the other team has units and you don't have units there (or in adjacent columns) spawn there
        # if there is a column where the opponent is in the 4 ranks nearest you, spawn there
        for i in range(board_size):
            if check_space(index + 3 * forward, i) == opp_team:
                if not check_space(index, i) and not team == check_space(index + forward, i):
                    spawn(index, i)
        for i in range(board_size):
            if check_space(index + 4 * forward, i) == opp_team:
                if not check_space(index, i):
                    spawn(index, i)

        # if columns 0 through n have been won, then spawn in column n+1
        if team == check_space(15-index, 0):
            for i in range(15):
                if not (team == check_space(15-index, i+1)):
                    if not check_space(index, i+1): spawn(index, i+1)
                    if not check_space(index, i): spawn(index, i)
                    if i > 0 and not check_space(index, i-1): spawn(index, i-1)
                    if i > 1 and not check_space(index, i-2): spawn(index, i-2)
                    break
        if not check_space(index, 1):
            spawn(index, 1)
            dlog('Spawned unit at: (' + str(index) + ', ' + str(1) + ')')
        """
        if not check_space(index, 14):
            spawn(index, 14)
            dlog('Spawned unit at: (' + str(index) + ', ' + str(14) + ')')
        """
        if not check_space(index, 0):
            spawn(index, 0)
            dlog('Spawned unit at: (' + str(index) + ', ' + str(0) + ')')
        # spawn near sides at higher probability
        i = random.randint(0, board_size - 1)
        if (i <= 3 or i >= 12):
            if not check_space(index, i):
                spawn(index, i)
        for _ in range(100):
            i = random.randint(0, board_size - 1)
            if not check_space(index, i):
                spawn(index, i)
                dlog('Spawned unit at: (' + str(index) + ', ' + str(i) + ')')
                break

    bytecode = get_bytecode()
    dlog('Done! Bytecode left: ' + str(bytecode))

if robottype == RobotType.PAWN:
    turn = pawn_turn_wrapper
else:
    turn = overlord_turn
