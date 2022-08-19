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

def window_eval(window, piece): #makes it so we dont have to copy and paste 4 lines of code in each pos_score
	score = 0
	opp_piece = P_PIECE
	if piece == P_PIECE:
		opp_piece = A_PIECE

	if window.count(piece) == 4: #this sets a score to each move, to acquire a 1,2,3,4 in a row
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 10
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 5

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1: #this states; if opponent gets 3 in a row, AI losses 8 points
		score -= -8

	return score

def pos_score(layout, piece): # this function will count how many piece you have together, which will ensure you/AI wins
	score = 0

#make preferences for centering AI piece since it increases chances of winning
	center_array = [int(i) for i in list(layout[:, COL_TOTAL//2])] #floor divison by 2 will get you the center column
	center_count = center_array.count(piece)
	score += center_count * 6

	#Horizontal
	for r in range(ROW_TOTAL): #for each row this will happen:
		row_array = [int(i) for i in list(layout[r,:])] #added int i to make sure were not contradicting with a float
		for c in range(COL_TOTAL - 3): #this will look at all the window sizes of 4
			window = row_array[c:c+W_LENGTH]
			score += window_eval(window,piece)

	#Vertical 
	for c in range(COL_TOTAL):
		col_array = [int(i) for i in list(layout[:,c])]
		for r in range(ROW_TOTAL-3):
			window = col_array[r:r+W_LENGTH]
			score += window_eval(window,piece)

	#Diagnol(+)
	for r in range(ROW_TOTAL-3):#-3 because we have to cut off each row going up
		for c in range(COL_TOTAL-3): #this is going to the right each time so we have to cut off 3 here too
			window = [layout[r+i][c+i] for i in range(W_LENGTH)]
			score += window_eval(window,piece)

	#Diagnol(-)
	for r in range(ROW_TOTAL-3):
		for c in range(COL_TOTAL-3):
			window = [layout[r+3-i][c+1] for i in range(W_LENGTH)] #have to add 3 because you have to go up first to get a diagnol(-) connect 4
			#row decreases but column increases when diagnol(-)
			score += window_eval(window,piece)
	return score

def is_terminal_node(layout): #initializing a terminal node so its defined as either no valid moves, Player winning or AI winning 
	return is_winner(layout, P_PIECE) or is_winner(layout, A_PIECE)or len(check_valid(layout)) == 0 #player wins, AI wins, no valid moves, respectively

def minimax(layout,depth,alpha, beta, maximizingPlayer): #using pseudocode from wikipedia of minimax, and initializing alpha beta pruning using wiki as well
	#minimax algorithm basically looks into the future to determine the best possible "branch" to go into for the best score/result
	#maximizingPlayer will be true for the AI since the algo should favour the AI and false for the Player
	#mutually recursive since min calls max, and max calls min
	valid_locations = check_valid(layout)
	terminal_node = is_terminal_node(layout)
	if depth == 0 or terminal_node:
		if terminal_node:
			if is_winner(layout, A_PIECE): #if AI is about to win then it should be favoured with +10000 points
				return (None, 10000)
			elif is_winner(layout, P_PIECE):
				return (None, -10000) #if Player is about to win then it should be favoured with -10000 points
			else: #no valid moves left
				return (None, 0)
		else: #When depth is 0
			return (None,pos_score(layout, A_PIECE)) #this will find the heuristic value of board

	if maximizingPlayer:
		value = -math.inf #+/- inf is determined by pseudocode in the wiki
		col = random.choice(valid_locations) #initializing the choice to random 
		for column in valid_locations: #checks each column for valid locations
			row = open_row(layout,column)#checks each row for valid locations
			copy_board = layout.copy() #need to make a copy or it will use the same memory as the original board
			drop_piece(copy_board, row, column, A_PIECE) #drops piece in the "best" position
			new_score = minimax(copy_board, depth-1, alpha, beta, False)[1] #this 
			if new_score > value: #this calculates wether the current move will result in the best possible score
				value = new_score
				col = column
			alpha = max(alpha, value) #alpha beta pruning makes the algorithm alot faster since it will prune unneccessary branches 
			if alpha >= beta:
				break
		return col, value
	
	else: #Minimizing Player
		value = math.inf
		col = random.choice(valid_locations)
		for column in valid_locations:
			row = open_row(layout,column)
			copy_board = layout.copy()
			drop_piece(copy_board,row,column,P_PIECE)
			new_score = minimax(copy_board, depth-1, alpha, beta, True) [1]#the false and true statements allows us to switch between each minimax algorithm
			if new_score < value: #this calculates wether the players could make a move which would result in a lower score for the AI
				value = new_score
				col = column
			beta = min(beta,value)
			if alpha >= beta:
				break
		return col, value


def check_valid(layout): #this function will show the AI if the column chosen is a valid location
	valid_locations = []
	for column in range(COL_TOTAL):
		if is_valid(layout,column):
			valid_locations.append(column)
	return valid_locations

def best_move(layout, piece):
	valid_location = check_valid(layout) #this checks if chosen location is valid
	best_score = -2000 #to make sure the code doesnt crash if the AI total score goes below 0
	best_column = random.choice(valid_location) 
	for column in valid_location:
		row = open_row(layout, column) #this will evaluate each movie using the function
		temp_board = layout.copy() #have to make a copy since this will duplicate and moify the original board if we dont copy
		drop_piece(temp_board,row,column,piece)
		score = pos_score(temp_board,piece) 
		if score > best_score: #this says that if the score is greater than 0, then it will change the positions
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

turn = random.randint(PLAYER, AI) #this makes who goes first random 

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
			#took out yellow tile so the tile doesnt show up when its the AI's turn

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

					print_board(layout) #updates board so the delay we set works 
					draw_board(layout)


	#P2 input
	if turn == AI and not game_over:

		column, minimax_score = minimax(layout,6,-math.inf, math.inf, True) #this implements the minimax algorithm before outputting the AI move
		#greater depth will increase the time it takes for the AI to make a move, however using alpha beta pruning we can reduce this time significantly
		if is_valid(layout, column):
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
		pygame.time.wait(2500)
