import numpy as np
import pygame
import sys
import math

ROW_TOTAL = 6
COL_TOTAL = 7

def create_board():
    layout = np.zeros((ROW_TOTAL,COL_TOTAL))
    return layout

def drop_piece(layout, row, column, piece):
  layout[row][column] = piece

def is_valid(layout,column):
	return layout[5][column] == 0

def open_row(layout, column):
	for r in range(ROW_TOTAL):
	  if layout[r][column] == 0:
	    return r

def print_layout(layout):
  print(np.flip(layout,0))

layout = create_board()
print_layout(layout)
game_over = False
turn = 0

while not game_over:
  
	#Input for P1 
	if turn == 0:
		column = int(input("P1, Choose where you want to place your piece (0-6):"))
		if is_valid(layout,column):
		  row = open_row(layout, column)
		  drop_piece(layout, row, column, 1)

	#Input for P2
	
else: 
		column = int(input("P2, Choose where you want to place your piece (0-6):"))
		if is_valid(layout, column):
		  row = open(layout, column)
		  drop_piece(layout, row, column, 2)	
	  
print_layout(layout)
	
turn += 1
turn = turn%2
