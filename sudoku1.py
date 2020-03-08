#####################################
# sudoku.py
# Spring 2020
# By: Emil Polakiewicz
#
# Purpose: Used a constrained satisfaction approach to solve a sudoku puzzle
#
#####################################

import math

grid_size = 9
box_size = 3

class Grid:

    def __init__(self, board, con_satisfied):
        self.board = board
        self.con_satisfied = con_satisfied

    # checks if the entire board is filled
    def board_filled(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if (self.board[i][j] == 0):
                    return False
        return True

    # checks if value satisfies constrains when in cell
    def valid_cell(self, val, row, col):
        if not self.horiz_alldiff(val, row):
            return False
        elif not self.vert_alldiff(val, col):
            return False
        elif not self.box_alldiff(val, row, col):
            return False
        else:
            return True

    # checks alldiff constraint for rows
    def horiz_alldiff(self, val, row):
        counting_array = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        counting_array[val - 1] += 1

        # count number of appearances of each number
        for i in range(len(self.board[row])):
            if self.board[row][i] != 0:
                counting_array[self.board[row][i] - 1] += 1

        # constraint violated when more than one of a number
        for i in range(len(counting_array)):
            if counting_array[i] > 1:
                return False
        return True

    # checks alldiff constraint for columns
    def vert_alldiff(self, val, col):
        counting_array = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        counting_array[val - 1] += 1

        # count number of appearances of each number
        for i in range(len(self.board)):
            if self.board[i][col] != 0:
                counting_array[self.board[i][col] - 1] += 1

        # constraint violated when more than one of a number
        for i in range(len(counting_array)):
            if counting_array[i] > 1:
                return False
        return True

    # checks alldiff constraint for box
    def box_alldiff(self, val, row, col):
        counting_array = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        counting_array[val - 1] += 1

        # count number of appearances of each number
        for i in range((row // box_size) * box_size, (row // box_size) * box_size + box_size):
            for j in range((col // box_size) * box_size, (col // box_size) * box_size + box_size):
                if self.board[i][j] != 0:
                    counting_array[self.board[i][j] - 1] += 1

        # constraint violated when more than one of a number
        for i in range(len(counting_array)):
            if counting_array[i] > 1:
                return False
        return True
    
    # returns indices of first unassigned box
    def select_unassigned_var(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if not self.board[i][j] != 0:
                    return [i, j]

    # print out grid (CHANGE)
    def print_grid(self):
        for i in range(len(self.board)):
            if  i != 0 and (i % box_size) == 0:
                print("---------------------")
            for j in range(len(self.board[0])):
                if j != 0 and (j % box_size) == 0:
                    print("| ", end="")
                if (j == grid_size - 1):
                    if (self.board[i][j] == 0):
                        print("_")
                    else:
                        print(str(self.board[i][j]))
                else:
                    if (self.board[i][j] == 0):
                        print("_ ", end="")
                    else:
                        print(str(self.board[i][j]) + " ", end="")


def backtracking_search(grid):
    # base case: board is filled, we have a solution
    if grid.board_filled():
        return grid

    # Select next variable
    curr = grid.select_unassigned_var()
    row = curr[0]
    col = curr[1]

    # Try all possible values in the domain of var
    for i in range(1, 10):
        # assign value since it is valid
        if grid.valid_cell(i, row, col):
            grid.board[row][col] = i
            grid.con_satisfied = True
            # We have found a value that works, move on to the next one
            grid = backtracking_search(grid)
            if grid.con_satisfied:
                return grid
            # value does not work, reset var
            grid.board[row][col] = 0
    
    grid.con_satisfied = False
    return grid

def main():

    simpleBoard = Grid([
        [6,0,8,7,0,2,1,0,0],
        [4,0,0,0,1,0,0,0,2],
        [0,2,5,4,0,0,0,0,0],
        [7,0,1,0,8,0,4,0,5],
        [0,8,0,0,0,0,0,7,0],
        [5,0,9,0,6,0,3,0,1],
        [0,0,0,0,0,6,7,5,0],
        [2,0,0,0,9,0,0,0,8],
        [0,0,6,8,0,5,2,0,3]
    ], False)

    trickyBoard = Grid([
        [0,7,0,0,4,2,0,0,0],
        [0,0,0,0,0,8,6,1,0],
        [3,9,0,0,0,0,0,0,7],
        [0,0,0,0,0,4,0,0,9],
        [0,0,3,0,0,0,7,0,0],
        [5,0,0,1,0,0,0,0,0],
        [8,0,0,0,0,0,0,7,6],
        [0,5,4,8,0,0,0,0,0],
        [0,0,0,6,1,0,0,5,0]
    ], False)

    # take in input and find solution
    valid = False
    while not valid:
        choice = input('''Type "b" for basic puzzle, "t" for tricky puzzle: ''')
        valid = True
        if choice.lower() == 'b':
            print("Board:")
            simpleBoard.print_grid()
            print("\nSolution:")
            backtracking_search(simpleBoard)
            simpleBoard.print_grid()
        elif choice.lower() == 't':
            print("Board:")
            trickyBoard.print_grid()
            print("\nSolution:")
            backtracking_search(trickyBoard)
            trickyBoard.print_grid()
        else:
            print("Invalid Input:")
            valid = False

if __name__ == "__main__":
    main()
