#!/usr/bin/env python
# coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""

import sys
import random
import time

ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)

def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            #print(board[r+c])
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def backtracking(board):
    # set sol as a global value
    global sol

    # find all empty cells
    empty = get_empty(board)

    # if the board is completely filled in, we're done
    if len(empty) == 0:
        sol = board_to_string(board)
        return True

    # if the board is not filled, set constraints and find mrv cell
    constraint = find_constraint(board)
    cell = mrv(constraint, empty)
    values = constraint[cell]

    # check if there are no constraints; if no, proceed
    while len(values) != 0:
        # forward check
        v = random.choice(values)
        values.remove(v)
        
        if fc(cell[0], cell[1], v, constraint):
            board[cell] = v
            # recursive call to backtracking; if true, we're done
            done = backtracking(board)
            if done:
                sol = board_to_string(board)
                return True
            # if not true, reset to empty and continue
            else:
                board[cell] = 0
    return False

def mrv(constraint, empty):
    mrv_num = []
    for cell in empty:
        num = len(constraint[cell])
        mrv_num.append(num)
  
    low = min(mrv_num)
    i = mrv_num.index(low)
    return empty[i]

def fc(row, col, value, constraint):
    col_check = True
    row_check = True
    grid_check = True

    row_0 = int(ROW.find(row)/3)
    col_0 = int((int(col)-1)/3)

    for c in COL:
        if c != col:
          if len(constraint[row+c])== 1:
            if constraint[row+c][0] == value:
              col_check = False

    for r in ROW:
        if r != row:
          if len(constraint[r+col])== 1:
            if constraint[r+col][0] == value:
              row_check = False
    
    for i in range(row_0*3, row_0*3 + 3):
        for j in range(col_0*3, col_0*3 + 3):
            row_i = ROW[i]
            col_i = COL[j]
            if (row_i != row or col_i != col):
              if len(constraint[row_i + col_i]) == 1:
                if constraint[row_i + col_i][0]== value:
                  grid_check = False

    return (col_check and row_check and grid_check)

def get_empty(board):
    empty = []
    for key, val in board.items():
        if val == 0:
            empty.append(key)
    return empty

def find_constraint(board):
    constraint = {}

    for i in ROW:
        for j in COL:
            constraint[i+j] = [1,2,3,4,5,6,7,8,9]

    for i in ROW:
        for j in COL:
            if board[i+j] == 0:
                continue
            else:
                k = board[i+j]
                constraint = remove_value(i,j,k,constraint)
                
    return constraint

def remove_value(r, c, v, constraint): 
    row_0 = int(ROW.find(r)/3)
    col_0 = int((int(c)-1)/3)
    constraint[r+c] = [0]
    
    for i in COL:
        values = constraint[r+i]
        if v in values:
          values.remove(v)
    
    for j in ROW:
        values = constraint[j+c]
        if v in values:
            values.remove(v)

    for i in range(row_0*3, row_0*3 + 3):
        for j in range(col_0*3, col_0*3 + 3):
            row_i = ROW[i]
            col_i = COL[j]
            values = constraint[row_i + col_i]
            if v in values:
                values.remove(v)

    return constraint

def write(board, out_filename):
    backtracking(board)
    outfile = open(out_filename, 'w+')
    outfile.write(sol)
    outfile.write('\n')

    return sol

if __name__ == '__main__':
    if len(sys.argv) > 1:
        startime=time.time()/(60 * 1000000000)

        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        #print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = {ROW[r] + COL[c]: int(sys.argv[1][9 * r + c])
            for r in range(9) for c in range(9)}

        out_filename = 'output.txt'
        print(startime)
        write(board, out_filename)

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")       

        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):
            

            if len(line) < 9:
                continue

            # Parse boards to dict representation
            board = {ROW[r] + COL[c]: int(line[9 * r + c])
                    for r in range(9) for c in range(9)}
            
            # Print starting board. TODO: Comment this out when timing runs.
            #print_board(board)

            # Solve with backtracking
            solved_board = backtracking(board)

            # Print solved board. TODO: Comment this out when timing runs.
            #print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')

        print("Finished all boards in file.")
