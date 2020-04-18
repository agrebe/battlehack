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
    elif check_space_wrapper(row + forward, col - 1) == opp_team: # up and left
        capture_wrapper(row + forward, col - 1)
        dlog('Captured at: (' + str(row + forward) + ', ' + str(col - 1) + ')')
    # an edge bot can advance if it has a defender
    # TODO: Maybe also make sure the defender won't move out of the way?
    elif (col == 0 and team == check_space_wrapper(row, 1)) or (col == 15 and team == check_space_wrapper(row, 14)):
        move_forward_wrapper()
        dlog('Moved forward thanks to defender!')
    # if there is an enemy pawn (2,1) or (2,-1) away, don't move forward
    elif (opp_team == check_space_wrapper(row + 2*forward, col+1) or opp_team == check_space_wrapper(row + 2*forward, col-1)):
        dlog('Waiting, unit ahead:' + str(board[row+2*forward][col+1]) + ' ' + str(board[row+2*forward][col-1]))
        dlog('Waiting, unit ahead:' + str(check_space_wrapper(row + 2*forward, col+1)) + ' ' + str(check_space_wrapper(row + 2*forward, col-1)))
    # otherwise try to move forward
    elif row + forward != -1 and row + forward != board_size and not check_space_wrapper(row + forward, col):
        move_forward_wrapper()
        dlog('Moved forward!')
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
        if not check_space(index, 1):
            spawn(index, 1)
            dlog('Spawned unit at: (' + str(index) + ', ' + str(1) + ')')
        if not check_space(index, 14):
            spawn(index, 14)
            dlog('Spawned unit at: (' + str(index) + ', ' + str(14) + ')')
        for _ in range(board_size):
            i = random.randint(0, board_size - 1)
            if not check_space(index, i):
                spawn(index, i)
                dlog('Spawned unit at: (' + str(index) + ', ' + str(i) + ')')
                break

    bytecode = get_bytecode()
    dlog('Done! Bytecode left: ' + str(bytecode))

if robottype == RobotType.PAWN:
    turn = pawn_turn
else:
    turn = overlord_turn
