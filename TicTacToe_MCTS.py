from math import sqrt, log
from random import randint, shuffle
import copy
import os

c = sqrt(2)

def printGrid(grid):
    print(grid[0][0], '|', grid[0][1], '|', grid[0][2])
    print('----------')
    print(grid[1][0], '|', grid[1][1], '|', grid[1][2])
    print('----------')
    print(grid[2][0], '|', grid[2][1], '|', grid[2][2])
    print()

def turnCount(grid):
    count = 0
    for row in grid:
        for box in row:
            if box != ' ':
                count+=1
    return count

def checkWin(grid):
    turns = turnCount(grid)
    for i in range(3):
        if(grid[i][0] == grid[i][1] == grid[i][2] != ' '): return 10-turns if grid[i][0]=='X' else -10+turns
        if(grid[0][i] == grid[1][i] == grid[2][i] != ' '): return 10-turns if grid[0][i]=='X' else -10+turns
    if((grid[0][0] == grid[1][1] == grid[2][2] != ' ')
       or (grid[2][0] == grid[1][1] == grid[0][2] != ' ')):
        return 10-turns if grid[1][1]=='X' else -10+turns
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
    if checkWin(grid): return moves
    for i in range(3):
        for o in range(3):
            if grid[i][o]==' ':
                moves.append([i, o])
    return moves

symbol = ['X', 'O']

class Node:
    def __init__(self, grid, parent=None, turn=0):
        self.parent = parent
        self.grid = grid
        self.utility = 0
        self.visit = 0
        self.children = {}
        self.turn = turn

    def addState(self, newState):
        self.children[str(newState)] = Node(newState, parent=self, turn=1-self.turn)

    def rollout(self):
        board = copy.deepcopy(self.grid)
        player = self.turn
        while(checkWin(board)==None):
            moves = getPossibleMoves(board)
            randMove = randint(0, len(moves)-1)
            board = playTurn(board, moves[randMove], symbol[player])
            player = 1-player
        return checkWin(board)

    def selection(self):
        bestChild = None
        maxUCB = float("-inf")
        for child in self.children:
            curState = self.children[child]
            if curState.visit==0:
                return self.children[child]
            u = curState.utility
            n = curState.visit
            N = curState.parent.visit
            ucb1 = (u/n) + c*sqrt(log(N)/n)
            if ucb1>maxUCB:
                maxUCB = ucb1
                bestChild = curState
        return bestChild

    def expansion(self):
        moves = getPossibleMoves(self.grid)
        shuffle(moves)
        for move in moves:
            self.addState(playTurn(self.grid, move, symbol[self.turn]))

    def backpropagate(self, utility):
        curNode = self
        while curNode:
            curNode.visit+=1
            curNode.utility+=utility
            curNode = curNode.parent
            utility = -utility


def MonteCarlo(grid, turn, its = 1000):
    gameTree = Node(grid, turn=turn)
    for i in range(its):
        curNode = gameTree
        while(len(curNode.children)):
            curNode = curNode.selection()
        if curNode.visit>0 or curNode.parent==None:
            curNode.expansion()
            if len(curNode.children): curNode = curNode.selection()
        result = curNode.rollout()
        if curNode.turn==0: result=-result
        curNode.backpropagate(result)
    return gameTree

grid = [[' ', ' ', ' '],
        [' ', ' ', ' '],
        [' ', ' ', ' ']]
os.system('cls')
turn = input("Who starts? (0 for you, 1 for AI): ")
turn = int(turn)
while turn!=0 and turn!=1:
    turn = input("Who starts? (0 for you, 1 for AI): ")
    turn = int(turn)

os.system('cls')
while(checkWin(grid)==None):
    printGrid(grid)
    move=None
    if turn==0:
        move = input("Enter your move (row,column): ")
        move = move.split(',')
        while len(move)!=2 or move[0] not in ["0","1","2"] or move[1] not in ["0","1", "2"] or grid[int(move[0])][int(move[1])]!=' ':
            move = input("Enter your move (row,column): ")
            move = move.split(',')
        move[0] = int(move[0])
        move[1] = int(move[1])
        grid = playTurn(grid, move, symbol[turn])
    else:
        its = input("How many iterations should the AI do? ")
        while(not its.isnumeric() or int(its)<0):
            its = input("How many iterations should the AI do? ")
        gameTree = MonteCarlo(grid, turn, int(its))
        selection = max(gameTree.children, key = lambda key: gameTree.children[key].visit)
        selection = gameTree.children[selection]
        grid = selection.grid
    turn = 1-turn
    os.system('cls')
printGrid(grid)
winner = checkWin(grid)
if winner==0:
    print("It's a tie!")
else:
    print(f'X wins'if winner==1 else 'O wins')