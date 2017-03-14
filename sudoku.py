import random
import sys
import numpy as np

from search import *

class Sudoku(Problem):
    def actions(self, state):
        state = grid(state)
        for i, j in zip(*np.where(state == 0)):
            line = state[i]
            column = state[:,j]
            square = state[i//3*3:i//3*3+3,j//3*3:j//3*3+3]
            for elem in range(1, 10):
                if elem not in line and elem not in column and elem not in square:
                    yield i, j, elem

    def result(self, state, action):
        i, j, elem = action
        temp = list(state)
        temp[i*9+j] = elem
        return tuple(temp)

    def goal_test(self, state):
        return 0 not in state and not conflict(state)

    def value(self, state):
        state = grid(state)
        temp = []
        for i, j in zip(*np.where(state == 0)):
            temp += [possibilities(state, i, j)]
        return len(temp)

class SudokuHillClimbing(Problem):
    def __init__(self, initial, goal=None):
        state = grid(initial)
        self.initial = state
        for i, j in zip(*np.where(state == 0)):
            poss = possibilities(state, i, j)
            state[i][j] = random.choice(poss)
        self.filled = tuple(state.flatten())

    def actions(self, state):
        state = grid(self.initial)
        # Trouve un square
        for i, j in zip(*np.where(state == 0)):
            square = state[i//3*3:i//3*3+3,j//3*3:j//3*3+3]
            # On trouve 2 case qui valent 0
            for x, y in zip(*np.where(square == 0)):
                if (i, j) != (x, y):
                    yield i, j, x, y

    def result(self, state, action):
        i, j, x, y = action
        temp = list(state)
        temp[i*9+j], temp[x*9+y] = temp[x*9+y], temp[i*9+j]
        return tuple(temp)

    def goal_test(self, state):
        state = grid(state)
        for elem in range(1, 10):
            for x in state:
                if state[x].count(elem) > 1:
                    return False
                elif state[:,x].count(elem) > 1:
                    return False
        return True

############### Corrigee. Retourne simplement le nombre d econflits
############### Pour hillclimbing c correct car square n'aura aucun conflit
    def value(self, state):
        return count_conflict(state)

def grid(state):
    return np.array(state).reshape((9, 9))

def line(state, line, elem):
    state = grid(state)
    return state[line].count(elem) > 1

def column(state, column, elem):
    state = grid(state)
    return state[:,column].count(elem) > 1

def square(state, line, column, elem):
    state = grid(state)
    return state[line//3*3:line//3*3+3,col//3*3:col//3*3+3].count(elem) > 1

########## Compte le nombre de conflits total. Si aucun conflits dans square
########## alors on compte les conflits des lignes et colonnes
def count_conflict(state):
    countConflicts = 0
    for x in range(9):
        for y in range(1, 10):
            if (line(state, x, y)):
                countConflicts += 1
            elif (column(state, x, y)):
                countConflicts += 1
        for i in range(9):
            for j in range(9):
                for k in range(1, 10):
                    if (square(state, i, j, k)):
                        countConflicts +=1
    return countConflicts

def possibilities(state, i, j):
    n = [x for x in range(1, 10)]
    temp = []
    state = grid(state)
    #line = state[i]
    #column = state[:,j]
    square = state[i//3*3:i//3*3+3,j//3*3:j//3*3+3]
    for elem in n:
        if elem not in square: #elem not in line and elem not in column and 
            temp.append(elem)
    return temp

def main():
    with open("1sudoku.txt", 'r') as f:
        for line in f:
            s = Sudoku(tuple(map(int, line[:-1])))
            # print(possibilities(s.initial, 0, 0))
            s2 = SudokuHillClimbing(tuple(map(int, line[:-1])))
            print(grid(hill_climbing(s2)))

def h(state):
    i, j, k = state.action
    return possibilities(state, i, j)

main()