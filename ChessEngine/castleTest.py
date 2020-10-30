#Tyler Barnes
#Chess Engine
import GameState, minimax, re, time

#Values for pieces
pvalue = { 'P': 100, 'N': 300, 'B': 300, 'R': 500, 'Q': 900, 'K': 1000000 }

#Starting setup of the board (I change this for testing)
board_start = (
    '         \n'  #Padding for move validation
    '         \n'  
    ' r...k..r\n'  
    ' pppppppp\n'  
    ' ........\n'  
    ' ........\n'  
    ' ........\n'  
    ' ........\n'  
    ' PPPPPPPP\n' 
    ' RNBQK..R\n' 
    '         \n'  
    '         \n'  # Padding for move validation
)

#Variables to quickly and easily track out of bounds movement
botleft = 91
botright = 98
topleft = 21
topright = 28
board_max = 119

#Setting checkmate values in order to calculate checkmate in a certain number of moves (upper and lower bounds)
MATE_LOWER = pvalue['K'] - 10*pvalue['Q']
MATE_UPPER = pvalue['K'] + 10*pvalue['Q']

#Prepares the ai's move for printing
def move_print(i):
    y, x = divmod(i - botleft, 10)
    return chr(x + ord('a')) + str(-y + 1)

#Prints the board
def print_pos(pos):
    print()
    for i, row in enumerate(pos.board.split()):
	    print(' ', 8-i, ' '.join(p for p in row))
    print('    a b c d e f g h \n\n')

#Formats input for coordinate translation (2d to 1d and character to value)
def format(input):
    x, y = ord(input[0]) - ord('a'), int(input[1]) - 1
    return botleft + x - 10*y
	
def main():
	#Setting the history to the starting GameState
    hist = [GameState.GameState(board_start, 0, (True,True), (True,True), 0, 0)]
	#Creating an instanceo f the search
    searcher = minimax.Search()
	#Running the program indefinitely
    while True:
		#Printing the position after the ai's last move (or the starting GameState)
        print_pos(hist[-1])

		#If the player has a difference in evaluation that can only be caused by
		#the player king being taken the player has lost.
        if hist[-1].eval <= -MATE_LOWER:
            print("Game Over")
            break

        #Getting a move from the user
        move = None
        while move not in hist[-1].move_generation():
			#Regex to match a properly formmated move
            match = re.match('([a-h][1-8])'*2, input('Input a move: '))
			#If it matches
            if match:
				#Parse the move so it can be translated to the board
                move = format(match.group(1)), format(match.group(2))
            else:
                # Inform the user when invalid input (e.g. "help") is entered
                print("Invalid Move EX: e2e4")
        hist.append(hist[-1].move(move))

        #Make the move and then rotate and print to show its outcome
		#Have to rotate because the ai also rotates the map when making a move
        print_pos(hist[-1].rotate())

		#If the player has a difference in evaluation that can only be caused by
		#the ai king being taken the player has won.
        if hist[-1].eval <= -MATE_LOWER:
            print("You won")
            break

        #Wait for the engine to make a move, limiting the time it can take 
        start = time.time()
        for _depth, move, eval in searcher.search(hist[-1], hist):
            if time.time() - start > 1:
                break

        # The black player moves from a rotated position, so we have to
        # 'back rotate' the move before printing it.
        print("My move:", move_print(board_max-move[0]) + move_print(board_max-move[1]))
        hist.append(hist[-1].move(move))


if __name__ == '__main__':
    main()