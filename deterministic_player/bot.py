import random

DEBUG = 0
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

aggressive_wait = 10 # for edge bots and bots in column 1
timid_wait = 20 # for other bots


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
    global row, wait_counter
    move_forward()
    row += forward
    wait_counter = 0
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

def pawn_get_board():
    board = [[False]*board_size for r in range(board_size)]
    for r, c, bot in sense():
        board[r][c] = bot
    return board

def pawn_turn():
    global row, col, wait_counter
    dlog('My location is: ' + str(row) + ' ' + str(col))
    board = pawn_get_board()

    # try capturing pieces
    if check_space_wrapper(row + forward, col - 1) == opp_team: # up and left
        capture_wrapper(row + forward, col - 1)
        dlog('Captured at: (' + str(row + forward) + ', ' + str(col - 1) + ')')
        return
    if check_space_wrapper(row + forward, col + 1) == opp_team: # up and right
        capture_wrapper(row + forward, col + 1)
        dlog('Captured at: (' + str(row + forward) + ', ' + str(col + 1) + ')')
        return
    # if there is something right in front of you, just wait and don't increment counters
    if check_space_wrapper(row+forward,col):
        return
    # near the back, advance more aggressively (since checks above will fail)
    if ((row-2*forward < 0 or row-2*forward > 15)
            and ((col == 0 and team == check_space_wrapper(row, 1))
            or (col == 15 and team == check_space_wrapper(row, 14)))):
        try_move_forward(board)
        dlog("Moved forward since near back, on the side, and has one defender")
        return
    # an edge bot can advance if it has a defender
    # TODO: Maybe also make sure the defender won't move out of the way?
    # modification: make sure it has an entire row of defenders so that the attack doesn't fizzle
    if ((col == 0 and team == check_space_wrapper(row, 1) and team == check_space_wrapper(row-forward, 1) 
            and team == check_space_wrapper(row-2*forward, 1))  
            or (col == 15 and team == check_space_wrapper(row, 14) 
            and team == check_space_wrapper(row-forward, 14) 
            and team == check_space_wrapper(row-2*forward, 14))) and random.random():
        if (wait_counter >= aggressive_wait):
            try_move_forward(board)
            dlog('Moved forward thanks to defender!')
            return
        else:
            wait_counter += 1
    # bots in column 1 can also advance fairly aggressively
    if (col == 1) and ((team == check_space_wrapper(row, 0) and team == check_space_wrapper(row-forward,0) and team == check_space_wrapper(row-2*forward,0)) or (team == check_space_wrapper(row, 2) and team == check_space_wrapper(row-forward,2) and team == check_space_wrapper(row-2*forward,2))):
        if wait_counter >= timid_wait:
            try_move_forward(board)
            dlog('Moved forward thanks to defender stack!')
            return
        else:
            wait_counter += 1
    # other bots can advance if they have two defenders at least with some probability
    # bots in the back three ranks with two defenders should always advance (easy to replace, also makes room for new bots)
    if team == check_space_wrapper(row, col-1) and team == check_space_wrapper(row, col+1) and (col <= 3 or col >= 12):
        if (row-3*forward < 0 or row-3*forward > 15) or wait_counter >= timid_wait:
            try_move_forward(board)
            dlog('Moved forward thanks to two defenders!')
            return
        else:
            wait_counter += 1
    # if a pawn sees a wall of pawns to its left (all 10 visible squares occupied by friendly pawns)
    # and if that pawn is on the left half of the board, then advance
    # This seems like it should happen with probability 1
    if (col == 1):
        wall = True
        for i in range(5): wall = wall and (team == check_space_wrapper(row+i-2, col-1) or row+i-2 < 0 or row+i-2 > 15)
        if (wall):
            try_move_forward(board)
            dlog('Moved forward thanks to wall')
            return
    if (col > 1 and col < 8):
        wall = True
        for i in range(5):
            wall = wall and (team == check_space_wrapper(row+i-2, col-1) or row+i-2 < 0 or row+i-2 > 15)
        for i in range(5):
            wall = wall and (team == check_space_wrapper(row+i-2, col-2) or row+i-2 < 0 or row+i-2 > 15)
        if (wall):
            dlog('Moved forward thanks to thick wall')
            try_move_forward(board)
            return
    
    # if there is an enemy pawn (2,1) or (2,-1) away, don't move forward
    if (opp_team == check_space_wrapper(row + 2*forward, col+1) or opp_team == check_space_wrapper(row + 2*forward, col-1)):
        dlog('Waiting, unit ahead:' + str(check_space_wrapper(row + 2*forward, col+1)) + ' ' + str(check_space_wrapper(row + 2*forward, col-1)))
        return

    # otherwise try to move forward
    try_move_forward(board)
    dlog('Moved forward!')

def pawn_turn_wrapper():
    pawn_turn()
    bytecode = get_bytecode()
    dlog('Done! Bytecode left: ' + str(bytecode))

# a column is "dead" if it is won, all columns to the left are won, and columns n+1, n+2, and n+3 are won
def column_dead(n):
    dead=True
    for i in range(n+4):
        dead = dead and team == check_space(15-index, i)
    return dead

def overlord_turn():
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
                    return
        for i in range(board_size):
            if check_space(index + 4 * forward, i) == opp_team:
                if not check_space(index, i):
                    spawn(index, i)
                    return

        # if the enemy has a pawn in the back 4 ranks, spawn in that rank and those adjacent
        for i in range(board_size):
            for j in range(1, 4):
                if check_space(index + j * forward, i) == opp_team:
                    if not check_space(index, i):
                        spawn(index, i)
                        return
                    if i > 0 and not check_space(index, i-1):
                        spawn(index, i-1)
                        return
                    if i < 15 and not check_space(index, i+1):
                        spawn(index, i+1)
                        return

        # if a column is empty of friendly units, it should get at least one pawn
        for i in range(16):
            empty = True
            for j in range(16):
                empty = empty and not team == check_space(j,i)
            if empty:
                if not check_space(index, i):
                    spawn(index, i)
                    return

        # if the enemy has more units in the last 8 rows of a column than you do, spawn there
        for i in range(16):
            pawn_differential = 0
            for j in range(8):
                pawn = check_space(index + j*forward, i)
                if (pawn == team): pawn_differential -= 1
                if (pawn == opp_team): pawn_differential += 1
            if pawn_differential > 0:
                if not check_space(index, i):
                    spawn(index, i)
                    return
                # if the column is already won by opponent, give up
                if check_space(index, i) == opp_team:
                    pass
                # if the space is occupied, try spawning in neighbors
                elif i > 0 and not check_space(index, i-1):
                    spawn(index, i-1)
                    return
                elif i < 15 and not check_space(index, i+1):
                    spawn(index, i+1)
                    return

        # if a column has only one friendly pawn it should get a second one
        for i in range(16):
            pawn_counter = 0
            for j in range(16):
                if team == check_space(j,i): pawn_counter += 1
            if pawn_counter < 2:
                if not check_space(index, i): 
                    spawn(index, i)
                    return

        # if columns 0 through n have been won, then spawn in column n+1
        if team == check_space(15-index, 0):
            for i in range(15):
                if not (team == check_space(15-index, i+1)):
                    if not check_space(index, i+1):
                        spawn(index, i+1)
                        return
                    if not check_space(index, i):
                        spawn(index, i)
                        return
                    if i > 0 and not check_space(index, i-1):
                        spawn(index, i-1)
                        return
                    if i > 1 and not check_space(index, i-2):
                        spawn(index, i-2)
                        return
                    break
        if not check_space(index, 1) and not column_dead(1): 
            spawn(index, 1)
            return
        # try to spawn in columns 0-2 (preferentially in 1)
        randInt = random.randint(0, 5)
        if randInt < 4:
            if not check_space(index, 0) and not column_dead(0): 
                spawn(index, 0)
                return
        else:
            if not check_space(index, 2) and not column_dead(2): 
                spawn(index, 2)
                return
        if not check_space(index, 0) and not column_dead(0):
            spawn(index, 0)
            dlog('Spawned unit at: (' + str(index) + ', ' + str(0) + ')')
            return
        if not check_space(index, 2) and not column_dead(2):
            spawn(index, 2)
            dlog('Spawned unit at: (' + str(index) + ', ' + str(2) + ')')
            return
        # spawn near sides at higher probability
        i = random.randint(0, board_size - 1)
        if (i <= 3 or i >= 12):
            if not check_space(index, i) and not column_dead(i):
                spawn(index, i)
                return
        for _ in range(100):
            i = random.randint(0, board_size - 1)
            if not check_space(index, i) and not column_dead(i):
                spawn(index, i)
                dlog('Spawned unit at: (' + str(index) + ', ' + str(i) + ')')
                return
        # make sure we provably spawn if there is a space available
        for i in range(16):
            if not check_space(index, i):
                spawn(index, i)
                dlog('Spawned unit at: (' + str(index) + ', ' + str(i) + ')')
                return
            dlog("Failed to spawn anywhere (BAD)!")

def count_material():
    material = 0
    for row in get_board():
        for v in row:
            if v == team: material += 1
            elif v == opp_team: material -= 1
    if team == Team.WHITE:
        material -= roundNum % 2
    else:
        material -= (roundNum+1) % 2
    return material
def overlord_turn_wrapper():
    global roundNum
    roundNum += 1
    overlord_turn()
    # log even for prod runs
    if team == Team.WHITE:
        log('== WHITE MATERIAL ' + str(count_material()) + ' ==')
    else:
        log('== BLACK MATERIAL ' + str(count_material()) + ' ==')
    bytecode = get_bytecode()
    dlog('Done! Bytecode left: ' + str(bytecode))    

if robottype == RobotType.PAWN:
    turn = pawn_turn_wrapper
else:
    turn = overlord_turn_wrapper
