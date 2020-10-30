import collections
from itertools import count

#Evaluation of position for each pvalue
#	This is used for the ai to develope pieces throughout the game, if this
#was not implemented the ai would just look to take and never develop. 
pvalue = { 'P': 100, 'N': 300, 'B': 300, 'R': 500, 'Q': 900, 'K': 1000000 }
evaluation = {
	#Evaluation for pawns
    'P': ( 0,  0,  0,  0,  0,  0,  0,  0,
		   5, 10, 10,-20,-20, 10, 10,  5,
           5, -5,-10,  0,  0,-10, -5,  5,
           0,  0,  0, 20, 20,  0,  0,  0,
           5,  5, 10, 25, 25, 10,  5,  5,
          10, 10, 20, 30, 30, 20, 10, 10,
          50, 50, 50, 50, 50, 50, 50, 50,
		   0,  0,  0,  0,  0,  0,  0,  0),
	#Evaluation for knights
    'N': ( -50, -40, -30, -30, -30, -30, -40, -50,
           -40, -20,   0,   5,   5,   0, -20, -40,
           -30,   5,  10,  15,  15,  10,   5, -30,
           -30,   0,  15,  20,  20,  15,   0, -30,
           -30,   5,  15,  20,  20,  15,   0, -30,
           -30,   0,  10,  15,  15,  10,   0, -30,
           -40, -20,   0,   0,   0,   0, -20, -40,
           -50, -40, -30, -30, -30, -30, -40, -50),
	#Evaluation for bishops
    'B': ( -20, -10, -10, -10, -10, -10, -10, -20,
		   -10,   5,   0,   0,   0,   0,   5, -10,
           -10,  10,  10,  10,  10,  10,  10, -10,
           -10,   0,  10,  10,  10,  10,   0, -10,
           -10,   5,   5,  10,  10,   5,   5, -10,
           -10,   0,   5,  10,  10,   5,   0, -10,
           -10,   0,   0,   0,   0,   0,   0, -10,
           -20, -10, -10, -10, -10, -10, -10, -20),
	#Evaluation for rooks
    'R': (   0,  0,  0,  5,  5,  0,  0,  0,
			-5,  0,  0,  0,  0,  0,  0, -5,
			-5,  0,  0,  0,  0,  0,  0, -5,
			-5,  0,  0,  0,  0,  0,  0, -5,
			-5,  0,  0,  0,  0,  0,  0, -5,
			-5,  0,  0,  0,  0,  0,  0, -5,
			 5, 10, 10, 10, 10, 10, 10,  5,
			 0,  0,  0,  0,  0,  0,  0,  0),
	#Evaluation for queens
    'Q': (  -20, -10, -10, -5, -5, -10, -10, -20,
			-10,   0,   5,  0,  0,   0,   0, -10,
			-10,   5,   5,  5,  5,   5,   0, -10,
			  0,   0,   5,  5,  5,   5,   0,  -5,
             -5,   0,   5,  5,  5,   5,   0,  -5,
            -10,   0,   5,  5,  5,   5,   0, -10,
            -10,   0,   0,  0,  0,   0,   0, -10,
            -20, -10, -10, -5, -5, -10, -10, -20),
	#Evaluation for king
    'K': (   0,  50,  50, -50, -50,  50,  50,   0,
           -30,  10,  50,  50,  50,  50,  10, -30,
           -50,  10, -50,  50, -50,  30,  30, -30,
           -50,  50,  10,   0, -20,  10,   0, -50,
           -50, -30, -50, -30, -50, -50, -10, -50,
           -50, -30, -50, -50, -50, -30, -30, -30,
            0,   0,  -10, -50, -50, -20,  10,   0,
            10,  30,   0, -10,   0,   0,  40,  10),
}

#Joining the pirces and evaluations
for j, boardpos in evaluation.items():
	#Adding in spacing using list comprehension to catch moves outside of the board
    spacing = lambda row: (0,) + tuple(x+pvalue[j] for x in row) + (0,)
    evaluation[j] = sum((spacing(boardpos[i*8:i*8+8]) for i in range(8)), ())
    evaluation[j] = (0,)*20 + evaluation[j] + (0,)*20

# How each piece can move (for player) for example, pawns can move up 1 or 2 moves
#this translates to -10 or -20 on the board because the player is oriented at the bottom.
#Pawns can also move diagonal to take pieces,this translates to -9 or -11 depending on which diagonal.  
move_list = {
    'P': (-10, -10+-10, -10+-1, -10+1),
    'N': (-10+-10+1, 1+-10+1, 1+10+1, 10+10+1, 10+10+-1, -1+10+-1, -1+-10+-1, -10+-10+-1),
    'B': (-10+1, 10+1, 10+-1, -10+-1),
    'R': (-10, 1, 10, -1),
    'Q': (-10, 1, 10, -1, -10+1, 10+1, 10+-1, -10+-1),
    'K': (-10, 1, 10, -1, -10+1, 10+1, 10+-1, -10+-1)
}

#Variables to quickly and easily track out of bounds movement
botleft = 91
botright = 98
topleft = 21
topright = 28
board_max = 119

# Class to hold the game state
#board = the representation of the board
#eval = the total evaluation of the gamestate
#w_castle = if the white pieces can castle
#b_castle = if the black pieces can castle
#enpass = the square that can be attacked using en passant
#mov_castle = the sqare being used for castling
class GameState(collections.namedtuple('GameState', 'board eval w_castle b_castle enpass mov_castle')):
	#Move generation
    def move_generation(self):
        #For each piece look at its possible moves
        for i, p in enumerate(self.board):
			#Only check moves for lower case pieces
            if not p.isupper(): continue
            for d in move_list[p]:
                for j in count(i+d, d):
					#Creating a local instance of the board
                    q = self.board[j]
                    #Making sure pieces stay on the board and don't stack
                    if q.isspace() or q.isupper(): break
                    #Normal pawn move
                    if p == 'P' and d in (-10, -10+-10) and q != '.': break
					#Pawn moving 2 spaces but only if it's on its starting square
                    if p == 'P' and d == -10+-10 and (i < botleft+-10 or self.board[i+-10] != '.'): break
					#Capturing a piece with a pawn
                    if p == 'P' and d in (-10+-1, -10+1) and q == '.' and j not in (self.enpass, self.mov_castle, self.mov_castle-1, self.mov_castle+1): break
                    # Actually moving the pawn
                    yield (i, j)
                    # Preventing overlapping movement of enemy pieces 
                    if p in 'PNK' or q.islower(): break
                    # Castling
                    if i == botleft and self.board[j+1] == 'K' and self.w_castle[0]: yield (j+1, j+-1)
                    if i == botright and self.board[j+-1] == 'K' and self.w_castle[1]: yield (j+-1, j+1)

	#Rotates the board for the ai so that the evaluations work for both colored pieces
    def rotate(self):
        return GameState(
			#Rotating the board and maintaining caslting and en passant rights
            self.board[::-1].swapcase(), -self.eval, self.b_castle, self.w_castle, 
			board_max-self.enpass if self.enpass else 0, board_max-self.mov_castle if self.mov_castle else 0)

	#Rotates the board but does not preverse en passant and castling rights
    def nullmove(self):
        return GameState(self.board[::-1].swapcase(), -self.eval, self.b_castle, self.w_castle, 0, 0)

	#AI actually making moves on the board
    def move(self, move):
		#Positions of the move
        i, j = move
		#What is currently on those squares on the board
        p, q = self.board[i], self.board[j]
        put = lambda board, i, p: board[:i] + p + board[i+1:]
        #Create a copy of the board
        board = self.board
		#reset the en passant rights
        w_castle, b_castle, enpass, mov_castle = self.w_castle, self.b_castle, 0, 0
		#Take ane evaluation of the move
        eval = self.eval + self.value(move)
        #Make the move
        board = put(board, j, board[i])
        board = put(board, i, '.')
        #Checking Castling Rights
        if i == botleft: w_castle = (False, w_castle[1])
        if i == botright: w_castle = (w_castle[0], False)
        if j == topleft: b_castle = (b_castle[0], False)
        if j == topright: b_castle = (False, b_castle[1])
        #Actually Castling
        if p == 'K':
			#Removing castling rights
            w_castle = (False, False)
			#Moving the rook
            if abs(j-i) == 2:
                mov_castle = (i+j)//2
                board = put(board, botleft if j < i else botright, '.')
                board = put(board, mov_castle, 'R')
        # Pawn promotion
        if p == 'P':
			#Autopromotion to queen for simplicity
            if topleft <= j <= topright:
                board = put(board, j, 'Q')
			#Double move if at starting position
            if j - i == 2*-10:
                enpass = i + -10
			#Taking en passant
            if j == self.enpass:
                board = put(board, j+10, '.')
        #Rotate the board back so that the next player can go
        return GameState(board, eval, w_castle, b_castle, enpass, mov_castle).rotate()
	
	#Confirming moves based on value
    def value(self, move):
		#Positions of the move
        i, j = move
		#What is currently on those squares on the board
        p, q = self.board[i], self.board[j]
        #Evaluating the move
        eval = evaluation[p][j] - evaluation[p][i]
        #Capturing pieces
        if q.islower():
            eval += evaluation[q.upper()][board_max-j]
        #Checking castling through check
        if abs(j-self.mov_castle) < 2:
            eval += evaluation['K'][board_max-j]
        #Evaluating castling
        if p == 'K' and abs(i-j) == 2:
            eval += evaluation['R'][(i+j)//2]
            eval -= evaluation['R'][botleft if j < i else botright]
        if p == 'P':
			#Checking pawn promotion
            if topleft <= j <= topright:
                eval += evaluation['Q'][j] - evaluation['P'][j]
			#Checking en passant
            if j == self.enpass:
                eval += evaluation['P'][board_max-(j+10)]
        return eval