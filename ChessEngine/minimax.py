import collections

#Values for pieces
pvalue = { 'P': 100, 'N': 300, 'B': 300, 'R': 500, 'Q': 900, 'K': 1000000 }

#Setting checkmate values in order to calculate checkmate in a certain number of moves (upper and lower bounds)
MATE_LOWER = pvalue['K'] - 10*pvalue['Q']
MATE_UPPER = pvalue['K'] + 10*pvalue['Q']

Start = collections.namedtuple('Start', 'lower upper')

#Maxval
MAXVAL = 100000000

#Class that will do the minimax search finding best moves.
#Uses the mtd-f algortihm checking upper and lower bounds (https://en.wikipedia.org/wiki/MTD-f)
#Also uses the killer hueristic for pruning (https://www.chessprogramming.org/Killer_Heuristic)
class Search:
    def __init__(self):
		#List for storing evaluations
        self.ai_eval = {}
		#List for storing moves
        self.ai_move = {}
		#Set for storing past moves
        self.history = set()
		#Game pos_moves that track possible moves
        self.pos_moves = 0

	#Returns the best move of a bounded call
    def bound(self, pos, gamma, depth, root=True):
        self.pos_moves += 1

        #Since you have to take the king to end the game we have to check that the
		#king is still alive.
        if pos.eval <= -MATE_LOWER:
            return -MATE_UPPER

        #Check to see if we have already searched this position
        start = self.ai_eval.get((pos, depth, root), Start(-MATE_UPPER, MATE_UPPER))
		#If it is a new position
        if start.lower >= gamma and (not root or self.ai_move.get(pos) is not None):
            return start.lower
		#If it is an old position
        if start.upper < gamma:
            return start.upper

        #Generator of moves to search in order.
        #Lets us create moves but only calculate them if necessary
        def moves():
            #First try doing nothing in order to avoid a situation where the engine won't make a move
			#because any move would cause the boardstate to get worse
            if depth > 0 and not root and any(c in pos.board for c in 'RBNQ'):
                yield None, -self.bound(pos.nullmove(), 1-gamma, depth-3, root=False)
            # Null move
            if depth == 0:
                yield None, pos.eval
            #Pruning based on a move that gives the best result given a certain cutoff
			#I manually set that subjective cutoff to be a value of 200, moves that reach this evaluation
			#will cause other nodes to be pruned.
            prune = self.ai_move.get(pos)
			#Checking if the position given the value of the pruning move beats our cutoff
            if prune and (depth > 0 or pos.value(prune) >= 200):
                yield prune, -self.bound(pos.move(prune), 1-gamma, depth-1, root=False)
            #Checks all other moves that have not been pruned
            for move in sorted(pos.move_generation(), key=pos.value, reverse=True):
                #If the depth is 0 it only looks for moves that reach our cutoff value for pruning
                if depth > 0 or pos.value(move) >= 200:
                    yield move, -self.bound(pos.move(move), 1-gamma, depth-1, root=False)

        #Keep track of the best move
        best = -MATE_UPPER
        for move, eval in moves():
			#Continue to evaluate looking for the best move
            best = max(best, eval)
            if best >= gamma:
                #Need to clear to make sure we always have a move
                if len(self.ai_move) > MAXVAL: self.ai_move.clear()
                #Save the move
                self.ai_move[pos] = move
                break

        #Need to clear to make sure we always have a move
        if len(self.ai_eval) > MAXVAL: self.ai_eval.clear()
        #Creating the final table with our movelist
        if best >= gamma:
            self.ai_eval[pos, depth, root] = Start(best, start.upper)
        if best < gamma:
            self.ai_eval[pos, depth, root] = Start(start.lower, best)
		
		#Returning the best move found
        return best

	#Iterative deepening
    def search(self, pos, history=()):
		#Initializing possible moves and history
        self.pos_moves = 0
        self.history = set(history)
        #Clearing the table
        self.ai_eval.clear()

        #Binding the depth to a reasonable limit
        for depth in range(1, 10):
            #Binary search to find the highest score at the position
            lower, upper = -MATE_UPPER, MATE_UPPER
            while lower != upper:
				#Setting the gamma
                gamma = (lower+upper+1)//2
				#Getting an evaluation for the bounded search
                eval = self.bound(pos, gamma, depth)
				#Checking if the move is better or worse
                if eval >= gamma:
                    lower = eval
                if eval < gamma:
                    upper = eval
            #Make sure that a move is always played
            self.bound(pos, lower, depth)
            #Retrieve the move from the table
            yield depth, self.ai_move.get(pos), self.ai_eval.get((pos, depth, True)).lower