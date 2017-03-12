# Auteurs: Alexandre Brilhante, Yan Lajeunesse

from search import *
from utils import *

problem = [[None for x in range(9)] for y in range(9)]

class Sudoku(Problem):
    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def goal_test(self, state):
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def value(self, state):
        raise NotImplementedError

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
    return problem

def line_conflict(line, elem):
    for j in range(len(problem)):
        if problem[line][j] == elem:
            return True
    return False

def column_conflict(column, elem):
    for i in range(len(problem)):
        if problem[i][column] == elem:
            return True
    return False

def subsquare_conflict(line, column, elem):
    line -= line%3
    column -= column%3
    for i in range(3):
        for j in range(3):
            if problem[i+line][j+column] == elem:
                return True
    return False

def insert_conflict(line, column, elem):
    return False if not line_conflict(line, elem) and not column_conflict(column, elem) and subsquare_conflict(line, column, elem) else True

def possibilities(line, column):
    n = [x for x in range(1, 10)]
    for i in range(len(problem)):
        if problem[line][i] in n:
            n.remove(problem[line][i])      
    for i in range(len(problem)):
        if problem[i][column] in n:
            n.remove(problem[i][column])
    line -= line % 3
    column -= column % 3
    for i in range(3):
        for j in range(3):
            if problem[i+line][j+column] in n:
                n.remove(problem[i+line][j+column])
    return n