import numpy as np
import random
import pygame
import sys
import math

BLUE = (0,0,205)
GRAY = (5,5,5)
RED = (238,44,44)
YELLOW = (255,193,37)

ROW_TOTAL = 6 #total number of rows
COL_TOTAL = 7 #total number of columns
PLAYER = 0
AI = 1

EMPTY = 0
W_LENGTH = 4
P_PIECE = 1
A_PIECE = 2

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

def evaluate_window(window, piece):
	score = 0
	opp_piece = P_PIECE
	if piece == P_PIECE:
		opp_piece = A_PIECE
	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2
	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4
	return score

def pos_score(layout, piece):
	score = 0

	#Horizontal
	for r in range(ROW_TOTAL):
		row_array = [int(i) for i in list(layout[r,:])]
		for c in range(COL_TOTAL - 3):
			window = row_array[c:c+W_LENGTH]
			if window.count(piece) == 4:
				score += 100
			elif window.count(piece) == 3 and window.count(EMPTY) == 1:
				score += 10

	return score

def check_valid(layout):
	valid_locations = []
	for column in range(COL_TOTAL):
		if is_valid(layout,column):
			valid_locations.append(column)
	return valid_locations

def best_move(layout, piece):
	valid_location = check_valid(layout)
	best_score = 0
	best_column = random.choice(valid_location)
	for column in valid_location:
		row = open_row(layout, column)
		temp_board = layout.copy()
		drop_piece(temp_board,row,column,piece)
		score = pos_score(temp_board,piece)
		if score > best_score:
			best_score = score
			best_column = column
	return best_column



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
			if layout[r][c] == P_PIECE:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), h-int(r*SQUARESIZE+SQUARESIZE/2)), RAD)
			elif layout[r][c] == A_PIECE:
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), h-int(r*SQUARESIZE+SQUARESIZE/2)), RAD)
	pygame.display.update() #ensure pygame updates the display so we changes

layout = create_board()
print_board(layout)
game_over = False #determining when the game will be over

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

turn = random.randint(PLAYER, AI)

while not game_over:

	#This will exit out of the game once you click the [X], this function performs a system exit
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen,GRAY, (0,0, w, SQUARESIZE))
			posx = event.pos[0]
			if turn == PLAYER:
				pygame.draw.circle(screen,RED,(posx, int(SQUARESIZE/2)), RAD)
			pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen,GRAY, (0,0, w, SQUARESIZE))
			#print(event.pos) #this function will show where our mouse is clicking


			#P1 input

			if turn == PLAYER:
				posx = event.pos[0]
				column = int(math.floor(posx/SQUARESIZE))

				if is_valid(layout, column):
					row = open_row(layout, column)
					drop_piece(layout, row, column, P_PIECE)

					if is_winner(layout, P_PIECE):
						label = myfont.render("Congratulations! P1 has won.",1, RED)
						screen.blit(label,(40,10))
						game_over = True
						
					turn += 1
					turn = turn % 2	

					print_board(layout)
					draw_board(layout)


	#P2 input
	if turn == AI and not game_over:
		#column = random.randint(0, COL_TOTAL-1)
		column = best_move(layout, A_PIECE)

		if is_valid(layout, column):
			pygame.time.wait(500)
			row = open_row(layout, column)
			drop_piece(layout, row, column, A_PIECE)

			if is_winner(layout, A_PIECE):
				label = myfont.render("Congratulations! P2 has won.",1, YELLOW)
				screen.blit(label,(40,10))
				game_over = True

			print_board(layout)
			draw_board(layout)

			turn += 1
			turn = turn % 2	

	if game_over:
		pygame.time.wait(2000)
