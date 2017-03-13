# Auteurs: Alexandre Brilhante, Yan Lajeunesse

from search import *
from utils import *

problem = [[None for x in range(9)] for y in range(9)]

class Sudoku(Problem):
    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = set_goal()

    def set_goal(self):
        if value(self, state) == 0:
            if grid_full(state):
                self.goal = state

    def actions(self, state):
        temp = []
        for i in range(0, len(state)):
            for j in range(0, len(state)):
                if state[i][j] == 0:
                    for k in range(1, 10):
                        temp.append((i, j, k))
        return temp

    # Dépend de actions.
    def result(self, state, action):
        i, j, elem = action
        state[i][j] = elem
        return state

    # Retourne le total de conflits, on procède avec le min. Faut ajuster argmin...
    def value(self, state):
        raise NotImplementedError

    def grid_full(self, state):
        for i in range(9):
            for j in range(9):
                if state[i][j] == 0:
                    return False
        return True

def initialize_grid():
    temp = []
    with open("1sudoku.txt") as file:
        for line in file:
            l = line.strip()
            for i in range(0, len(l), 9):
                temp.append(l[i:i+9])
    for i in range(0, len(temp)):
        for j in range(0, len(temp[i])):
            problem[i][j] = int(temp[i][j:j+1])
    print(problem)
    return problem

# Retourne le nombre de conflits.
def line_conflict(line, elem):
    conflict = 0
    for j in range(len(problem)):
        if problem[line][j] == elem:
            conflict += 1
    return conflict

# Retourne le nombre de conflits.
def column_conflict(column, elem):
    conflict = 0
    for i in range(len(problem)):
        if problem[i][column] == elem:
            conflict += 1
    return conflict

# Retourne le nombre de conflits.
def subsquare_conflict(line, column, elem):
    conflict = 0
    line -= line%3
    column -= column%3
    for i in range(3):
        for j in range(3):
            if problem[i+line][j+column] == elem:
                conflict += 1
    return conflict

def insert_conflict(line, column, elem):
    return False if not line_conflict(line, elem) and not column_conflict(column, elem) and not subsquare_conflict(line, column, elem) else True

def possibilities(line, column):
    n = [x for x in range(1, 10)]
    for i in range(len(problem)):
        if problem[line][i] in n:
            n.remove(problem[line][i])
    for i in range(len(problem)):
        if problem[i][column] in n:
            n.remove(problem[i][column])
    line -= line%3
    column -= column%3
    for i in range(3):
        for j in range(3):
            if problem[i+line][j+column] in n:
                n.remove(problem[i+line][j+column])
    return n