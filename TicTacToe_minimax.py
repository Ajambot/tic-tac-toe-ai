import copy
import os

def printGrid(grid):
    print(grid[0][0], '|', grid[0][1], '|', grid[0][2])
    print('----------')
    print(grid[1][0], '|', grid[1][1], '|', grid[1][2])
    print('----------')
    print(grid[2][0], '|', grid[2][1], '|', grid[2][2])
    print()


def checkWin(grid):
    for i in range(3):
        if(grid[i][0] == grid[i][1] == grid[i][2] != ' '): return 1 if grid[i][0]=='X' else -1
        if(grid[0][i] == grid[1][i] == grid[2][i] != ' '): return 1 if grid[0][i]=='X' else -1
    if((grid[0][0] == grid[1][1] == grid[2][2] != ' ')
       or (grid[2][0] == grid[1][1] == grid[0][2] != ' ')):
        return 1 if grid[1][1]=='X' else -1
    for row in grid:
        for box in row:
            if(box == ' '):
                return None
    return 0

def playTurn(grid, position, symbol):
    newGrid = copy.deepcopy(grid)
    newGrid[position[0]][position[1]] = symbol
    return newGrid

def getPossibleMoves(grid):
    moves = []
    if checkWin(grid)!=None: return moves
    for i in range(3):
        for o in range(3):
            if grid[i][o]==' ':
                moves.append([i, o])
    return moves

symbol = ['X', 'O']
def minimax(grid, turn):
    if checkWin(grid)!=None:
        return checkWin(grid)
    maxOutcome = -2
    minOutcome = 2
    moves = getPossibleMoves(grid)
    for move in moves:
        i = move[0]
        o = move[1]
        if(grid[i][o]==' '):
            if(turn==0):
                maxOutcome = max(maxOutcome, minimax(playTurn(grid, [i, o], symbol[turn]), 1-turn))
            else:
                minOutcome = min(minOutcome, minimax(playTurn(grid, [i, o], symbol[turn]), 1-turn))
    return maxOutcome if turn==0 else minOutcome


memo = {}
def minimax_memo(grid, turn):
    if str(grid) in memo:
        return memo[str(grid)]
    if checkWin(grid)!=None:
        memo[str(grid)] = checkWin(grid)
        return memo[str(grid)]
    maxOutcome = -2
    minOutcome = 2
    moves = getPossibleMoves(grid)
    for move in moves:
        i = move[0]
        o = move[1]
        if(grid[i][o]==' '):
            if(turn==0):
                maxOutcome = max(maxOutcome, minimax_memo(playTurn(grid, [i, o], symbol[turn]), 1-turn))
            else:
                minOutcome = min(minOutcome, minimax_memo(playTurn(grid, [i, o], symbol[turn]), 1-turn))
    memo[str(grid)] = maxOutcome if turn==0 else minOutcome
    return memo[str(grid)]


def alpha_beta_memo(grid, turn, alpha, beta):
    if str(grid) in memo:
        return memo[str(grid)]
    if checkWin(grid)!=None:
        memo[str(grid)] = checkWin(grid)
        return memo[str(grid)]
    maxOutcome = -2
    minOutcome = 2
    moves = getPossibleMoves(grid)
    for move in moves:
        i = move[0]
        o = move[1]
        if(grid[i][o]==' '):
            if(turn==0):
                maxOutcome = max(maxOutcome, alpha_beta_memo(playTurn(grid, [i, o], symbol[turn]), 1-turn, alpha, beta))
                alpha = max(maxOutcome, alpha)
                if beta<=alpha: break
            else:
                minOutcome = min(minOutcome, alpha_beta_memo(playTurn(grid, [i, o], symbol[turn]), 1-turn, alpha, beta))
                beta = min(minOutcome, beta)
                if beta<=alpha: break
    memo[str(grid)] = maxOutcome if turn==0 else minOutcome
    return memo[str(grid)]

def alpha_beta(grid, turn, alpha, beta):
    if checkWin(grid)!=None:
        return checkWin(grid)
    maxOutcome = -2
    minOutcome = 2
    moves = getPossibleMoves(grid)
    for move in moves:
        i = move[0]
        o = move[1]
        if(grid[i][o]==' '):
            if(turn==0):
                maxOutcome = max(maxOutcome, alpha_beta(playTurn(grid, [i, o], symbol[turn]), 1-turn, alpha, beta))
                alpha = max(maxOutcome, alpha)
                if beta<=alpha: break
            else:
                minOutcome = min(minOutcome, alpha_beta(playTurn(grid, [i, o], symbol[turn]), 1-turn, alpha, beta))
                beta = min(minOutcome, beta)
                if beta<=alpha: break
    return maxOutcome if turn==0 else minOutcome


grid = [[' ', ' ', ' '],
        [' ', ' ', ' '],
        [' ', ' ', ' ']]
os.system('cls')
start = input("Who starts? (0 for you, 1 for AI): ")
start = int(start)
while start!=0 and start!=1:
    start = input("Who starts? (0 for you, 1 for AI): ")
    start = int(start)

os.system('cls')
models = [minimax, minimax_memo, alpha_beta, alpha_beta_memo]
sel = input("Select an AI to use (0: minimax, 1: minimax with memoization "
            + "2: alpha beta, 3: alpha beta with memoization): ")
while sel not in ["0", "1", "2", "3"]:
    sel = input("Select an AI to use (0: alpha beta, 1: alpha beta with memoization "
            + "2: minimax, 3: minimax with memoization): ")
sel = int(sel)
model = models[sel]
turn = start
while(checkWin(grid)==None):
    printGrid(grid)
    move=None
    if turn==0:
        move = input("Enter your move (x,y): ")
        move = move.split(',')
        while len(move)!=2 or move[0] not in ["0","1","2"] or move[1] not in ["0","1", "2"] or grid[int(move[0])][int(move[1])]!=' ':
            move = input("Enter your move (x,y): ")
            move = move.split(',')
        move[0] = int(move[0])
        move[1] = int(move[1])
        grid = playTurn(grid, move, symbol[turn])
    else:
        bestMove = None
        bestOutcome = 2
        for move in getPossibleMoves(grid):
            if start == 1 and sel<2:
                outcome = model(playTurn(grid, move, symbol[turn]), 1-turn)
                if outcome<bestOutcome:
                    bestOutcome = outcome
                    bestMove = move
            elif start==0 and sel<2:
                outcome = model(playTurn(grid, move, symbol[turn]), 1-turn)
                if outcome<bestOutcome:
                    bestOutcome = outcome
                    bestMove = move
            elif start==1 and sel>=2:
                outcome = model(playTurn(grid, move, symbol[turn]), 1-turn, -2, 2)
                if outcome<bestOutcome:
                    bestOutcome = outcome
                    bestMove = move
            elif start==0 and sel>=2:
                outcome = model(playTurn(grid, move, symbol[turn]), 1-turn, -2, 2)
                if outcome<bestOutcome:
                    bestOutcome = outcome
                    bestMove = move
        grid = playTurn(grid, bestMove, symbol[turn])
        os.system('cls')
    turn = 1-turn
printGrid(grid)
winner = checkWin(grid)
if winner==0:
    print("It's a tie!")
else:
    print(f'X wins'if winner==1 else 'O wins')