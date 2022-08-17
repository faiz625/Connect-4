import numpy as np
import pygame
import sys
import math

BLUE = (0,0,205)
GRAY = (5,5,5)
RED = (238,44,44)
YELLOW = (255,193,37)

ROW_TOTAL = 6 #total number of rows
COL_TOTAL = 7 #total number of columns

def create_board(): #creating the board/layout
	layout = np.zeros((ROW_TOTAL,COL_TOTAL)) #defining how many rows and columns there will be
	return layout

def drop_piece(layout, row, column, piece): #command to drop the piece into the slot
	layout[row][column] = piece

def open_row(layout, column): #checking to see if the row is open or not
	for r in range(ROW_TOTAL):
		if layout[r][column] == 0:
			return r

def is_valid(layout, column): #checking to see if chosen spot is valid
	return layout[ROW_TOTAL-1][column] == 0

def print_board(layout):
	print(np.flip(layout, 0))

def is_winner(layout, piece): #determines wether a player has won
	#checking if the player has won in horizontal, subtract by 3 because you cant have 4 
	#matches with 3 columns
	for c in range(COL_TOTAL-3): 
		for r in range(ROW_TOTAL):
			#each step checks wether there is a winner horizontally by going through them individually
			if layout[r][c] == piece and layout[r][c+1] == piece and layout[r][c+2] == piece and layout[r][c+3] == piece:
				return True
	#checking if the player has won in vertical
	for c in range(COL_TOTAL): 
		for r in range(ROW_TOTAL-3): #have to do -3 becuase we cant start at the top row
			#each step checks wether there is a winner horizontally by going through them individually
			if layout[r][c] == piece and layout[r+1][c] == piece and layout[r+2][c] == piece and layout[r+3][c] == piece:
				return True
	#checking if the player has won in diagnol(+)
	for c in range(COL_TOTAL-3): 
			for r in range(ROW_TOTAL-3): #have to do -3 becuase we cant start at the top row
				#each step checks wether there is a winner horizontally by going through them individually
				if layout[r][c] == piece and layout[r+1][c+1] == piece and layout[r+2][c+2] == piece and layout[r+3][c+3] == piece:
					return True
	#checking if the player has won in diagnol(-)
	for c in range(COL_TOTAL-3): 
			for r in range(3, ROW_TOTAL): #have to do 3, becuase the matches will start at the third index (middle of board)
				#each step checks wether there is a winner horizontally by going through them individually
				if layout[r][c] == piece and layout[r-1][c+1] == piece and layout[r-2][c+2] == piece and layout[r-3][c+3] == piece:
					return True

def draw_board(layout):
	for c in range(COL_TOTAL):
		for r in range(ROW_TOTAL):
			#You add by SQUARESIZE so it makes an empty space at the top instead of the bottom
			#defined BLUE in line5
			pygame.draw.rect(screen,BLUE,(c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE,SQUARESIZE,SQUARESIZE))
			#The position of the circles will have to have some offset from the rectangle, hence we add a SQUARESIZE/2 to each parameter
			#defined GRAY in line6
			#While using pygame you must use integers when determinig position/radius
			pygame.draw.circle(screen, GRAY, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RAD)
	
	for c in range(COL_TOTAL):
		for r in range(ROW_TOTAL):
			if layout[r][c] == 1:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), h-int(r*SQUARESIZE+SQUARESIZE/2)), RAD)
			elif layout[r][c] == 2:
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), h-int(r*SQUARESIZE+SQUARESIZE/2)), RAD)
	pygame.display.update() #ensure pygame updates the display so we changes

layout = create_board()
print_board(layout)
game_over = False #determining when the game will be over
turn = 0

pygame.init()
SQUARESIZE = 75
w = COL_TOTAL * SQUARESIZE
h = (ROW_TOTAL + 1) * SQUARESIZE
s = (w,h)
#You have to make the radius smaller than the SQUARESIZE
RAD = int(SQUARESIZE/2 - 3) #states the radius of the circles in the board/graphics

#acquiring functions for pygame.org/docs
screen = pygame.display.set_mode(s)
draw_board(layout)
pygame.display.update() #ensure pygame updates the display so we changes

myfont = pygame.font.SysFont("arial.ttf",40)

while not game_over:
	#This will exit out of the game once you click the [X], this function performs a system exit
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen,GRAY, (0,0, w, SQUARESIZE))
			posx = event.pos[0]
			if turn == 0:
				pygame.draw.circle(screen,RED,(posx, int(SQUARESIZE/2)), RAD)
			else:
				pygame.draw.circle(screen,YELLOW,(posx, int(SQUARESIZE/2)), RAD)
			pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen,GRAY, (0,0, w, SQUARESIZE))
			#print(event.pos) #this function will show where our mouse is clicking


			# #P1 input

			if turn == 0:
				posx = event.pos[0]
				column = int(math.floor(posx/SQUARESIZE))

				if is_valid(layout, column):
					row = open_row(layout, column)
					drop_piece(layout, row, column, 1)

					if is_winner(layout, 1):
						label = myfont.render("Congratulations! P1 has won.",1, RED)
						screen.blit(label,(40,10))
						game_over = True


			# #P2 input
			else:
				posx = event.pos[0]
				column = int(math.floor(posx/SQUARESIZE))

				if is_valid(layout, column):
					row = open_row(layout, column)
					drop_piece(layout, row, column, 2)

					if is_winner(layout, 2):
						label = myfont.render("Congratulations! P2 has won.",2, YELLOW)
						screen.blit(label,(40,10))
						game_over = True

			print_board(layout)
			draw_board(layout)

			turn += 1
			turn = turn % 2 #dividing by two to ensure the turns are alternating 

			if game_over:
				pygame.time.wait(4000)
