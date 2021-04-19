import pygame
import random
from convertFunc import nearBoardDot, numToBoardDotPos, boardDotPosToNum

# define colors
#                   R    G    B
white           = (255, 255, 255)
black           = (  0,   0,   0)
aquamarine3     = (102, 205, 170)
red             = (255,   0,   0)
blue            = (  0,   0, 255)

class Game:
	def __init__(self):
		self.user = 1
		self.ai = 0

		self.numDivision = 16
		self.numWin = 5
		self.boardWidth = 640
		self.boardHeight = 640
		self.cellSize = self.boardWidth // self.numDivision

		self.colorMatrix = [[None] * self.numDivision for
							i in range(self.numDivision)]
		self.aiScoreMatrix = [[0] * self.numDivision for 
							i in range(self.numDivision)]
		self.playerScoreMatrix = [[0] * self.numDivision for 
								i in range(self.numDivision)]
		self.scoreLevel = [0] + [10**i for i in range(7)]

		self.movements = []
		self.remain = set(range(1, (self.numDivision - 1)**2 + 1))

		self.aiPossibleList = []
		self.aiOptimalList = []
		self.aiTabuList = []

		self.playerOptimalSet = set()
		self.playerTabuList = []

		self.hitSound = pygame.mixer.Sound('chess.wav')
		self.hitSound.set_volume(0.1)

		self.clock = pygame.time.Clock()
		self.fps = 30


	"""
	CITATION:
	The idea of minimax and updating socre is from 
	https://blog.theofekfoundation.org/artificial-intelligence/2015/12/11/minimax-for-gomoku-connect-five/
	"""

	def updateScore(self, pos, color, iden):
	    # four directions to check
	    hori, slash, verti, backslash = 1, 1, 1, 1

	    left = pos[0] - 1
	    while left > 0 and self.colorMatrix[left][pos[1]] == color:
	        left -= 1
	        if hori == self.numWin - 1:
	            hori += 1
	            break
	        if left > 0 and (self.colorMatrix[left][pos[1]] == color or
	                    self.colorMatrix[left][pos[1]] is None):
	            hori += 1

	    right = pos[0] + 1
	    while right < self.numDivision and \
	    			self.colorMatrix[right][pos[1]] == color:
	        right += 1
	        if hori == self.numWin - 1:
	            hori += 1
	            break
	        if right < self.numDivision and \
	        		(self.colorMatrix[right][pos[1]] == color or
	                self.colorMatrix[right][pos[1]] is None):
	            hori += 1

	    hori = self.scoreLevel[hori]

	    up = pos[1] - 1
	    while up > 0 and self.colorMatrix[pos[0]][up] == color:
	        up -= 1
	        if verti == self.numWin - 1:
	            verti += 1
	            break
	        if up > 0 and \
	                (self.colorMatrix[pos[0]][up] == color or \
	                self.colorMatrix[pos[0]][up] is None):
	            verti += 1

	    down = pos[1] + 1
	    while down < self.numDivision and \
	    			self.colorMatrix[pos[0]][down] == color:
	        down += 1
	        if verti == self.numWin - 1:
	            verti += 1
	            break
	        if down < self.numDivision and \
	        		(self.colorMatrix[pos[0]][down] == color or
	                 self.colorMatrix[pos[0]][down] is None):
	            verti += 1

	    verti = self.scoreLevel[verti]

	    left = pos[0] - 1
	    up = pos[1] - 1
	    while left > 0 and up > 0 and self.colorMatrix[left][up] == color:
	        left -= 1
	        up -= 1
	        if backslash == self.numWin - 1:
	            backslash += 1
	            break
	        if left > 0 and up > 0 and\
	                (self.colorMatrix[left][up] == color or
	                    self.colorMatrix[left][up] is None):
	            backslash += 1

	    right = pos[0] + 1
	    down = pos[1] + 1
	    while right < self.numDivision and down < self.numDivision and \
	    			self.colorMatrix[right][down] == color:
	        right += 1
	        down += 1
	        if backslash == self.numWin - 1:
	            backslash += 1
	            break
	        if right < self.numDivision and down < self.numDivision and	\
	                (self.colorMatrix[right][down] == color or
	                    self.colorMatrix[right][down] is None):
	            backslash += 1

	    backslash = self.scoreLevel[backslash]

	    right = pos[0] + 1
	    up = pos[1] - 1
	    while right < self.numDivision and up > 0 and \
	    				self.colorMatrix[right][up] == color:
	        right += 1
	        up -= 1
	        if slash == self.numWin - 1:
	            slash += 1
	            break
	        if right < self.numDivision and up > 0 and \
	        			(self.colorMatrix[right][up] == color or
	                     self.colorMatrix[right][up] is None):
	            slash += 1

	    left = pos[0] - 1
	    down = pos[1] + 1
	    while left > 0 and down < self.numDivision and \
	    					self.colorMatrix[left][down] == color:
	        left -= 1
	        down += 1
	        if slash == self.numWin - 1:
	            slash += 1
	            break
	        if left > 0 and down < self.numDivision and \
	        		(self.colorMatrix[left][down] == color or
	                 self.colorMatrix[left][down] is None):
	            slash += 1

	    slash = self.scoreLevel[slash]
	    #print("updateScore", pos, color, iden, (hori, verti, slash, backslash))

	    if iden == self.user:
	        self.playerScoreMatrix[pos[0]][pos[1]] = \
	                            int((hori + verti + slash + backslash) * 0.9)
	    elif iden == self.ai:
	        self.aiScoreMatrix[pos[0]][pos[1]] = hori + verti + slash + backslash


	def gameIsOver(self, pos, color):
	    # four directions
	    hori, verti, slash, backslash = 1, 1, 1, 1

	    # check horizontal direction
	    left = pos[0] - 1
	    while left > 0 and self.colorMatrix[left][pos[1]] == color:
	        left -= 1
	        hori += 1

	    right = pos[0] + 1
	    while right < self.numDivision and \
	    			self.colorMatrix[right][pos[1]] == color:
	        right += 1
	        hori += 1

	    # check vertical direction
	    up = pos[1] - 1
	    while up > 0 and self.colorMatrix[pos[0]][up] == color:
	        up -= 1
	        verti += 1

	    down = pos[1] + 1
	    while down < self.numDivision and \
	    			self.colorMatrix[pos[0]][down] == color:
	        down += 1
	        verti += 1

	    # check backslash direction
	    left = pos[0] - 1
	    up = pos[1] - 1
	    while left > 0 and up > 0 and \
	    		self.colorMatrix[left][up] == color:
	        left -= 1
	        up -= 1
	        backslash += 1

	    right = pos[0] + 1
	    down = pos[1] + 1
	    while right < self.numDivision and down < self.numDivision and \
	    			self.colorMatrix[right][down] == color:
	        right += 1
	        down += 1
	        backslash += 1

	    # check slash direction
	    right = pos[0] + 1
	    up = pos[1] - 1
	    while right < self.numDivision and up > 0 and \
	    			self.colorMatrix[right][up] == color:
	        right += 1
	        up -= 1
	        slash += 1

	    left = pos[0] - 1
	    down = pos[1] + 1
	    while left > 0 and down < self.numDivision and \
	    			self.colorMatrix[left][down] == color:
	        left -= 1
	        down += 1
	        slash += 1

	    # check any of the four direction reach 5
	    if max(hori, verti, backslash, slash) >= 5:
	        return True


	def drawMovements(self, surf):
	    for move in self.movements[:-1]:
	        pygame.draw.circle(surf, move[1], move[0], int(self.boardWidth / 40))
	    if self.movements:
	        pygame.draw.circle(surf, aquamarine3, self.movements[-1][0], int(self.boardWidth / 40))

	def addChess(self, surf, color, pos, iden=1, radius=16):
	    self.movements.append(((int(pos[0] * self.cellSize), 
	    						int(pos[1] * self.cellSize)), color))
	    self.hitSound.play()

	    numPos = boardDotPosToNum(pos)
	    self.remain.remove(numPos)

	    if numPos in self.playerOptimalSet:
	        self.playerOptimalSet.remove(numPos)

	    self.playerScoreMatrix[pos[0]][pos[1]] = -1 - iden
	    self.aiScoreMatrix[pos[0]][pos[1]] = -1 - iden
	    self.colorMatrix[pos[0]][pos[1]] = color
	    
	    self.clock.tick(self.fps)

	    around = nearBoardDot(pos, 4)

	    for rx in range(around[0], around[1] + 1):
	        for ry in range(around[2], around[3] + 1):
	            numPos = boardDotPosToNum((rx, ry))
	            if numPos in self.remain:
	                self.updateScore((rx, ry), color, iden)
	                if color == black:
	                    tpcolor = white
	                else:
	                    tpcolor = black
	                self.updateScore((rx, ry), tpcolor, 1 - iden)

	def getNextMove(self, movements, currMove):
	    around = nearBoardDot((currMove[0][0] // self.cellSize,
	                          currMove[0][1] // self.cellSize))

	    for rx in range(around[0], around[1] + 1):
	        for ry in range(around[2], around[3] + 1):
	            numPos = boardDotPosToNum((rx, ry))
	            if numPos in self.remain:
	                self.playerOptimalSet.add(boardDotPosToNum((rx, ry)))

	    maxScore = -1000000
	    nextMove = 0

	    for i in self.playerOptimalSet:
	        boardDot = numToBoardDotPos(i)
	        if self.aiScoreMatrix[boardDot[0]][boardDot[1]] >= self.scoreLevel[5]:
	            nextMove = i
	            break
	        if self.playerScoreMatrix[boardDot[0]][boardDot[1]] >= self.scoreLevel[4]:
	            nextMove = i
	            break
	            
	        score = self.aiScoreMatrix[boardDot[0]][boardDot[1]] + self.playerScoreMatrix[boardDot[0]][boardDot[1]]

	        if score > maxScore:
	            maxScore = score
	            nextMove = i
	        elif maxScore == score:
	        	if (random.randint(0, 100) % 2) == 0:
	        		nextMove = i

	    around = nearBoardDot(numToBoardDotPos(nextMove))

	    for rx in range(around[0], around[1] + 1):
	        for ry in range(around[2], around[1] + 1):
	            numPos = boardDotPosToNum((rx, ry))
	            if numPos in self.remain:
	                self.playerOptimalSet.add(boardDotPosToNum((rx, ry)))
	                
	    return nextMove

	def respond(self, surf, movements, currMove):
	    nextMove = self.getNextMove(movements, currMove)
	    boardDotPos = numToBoardDotPos(nextMove)

	    self.addChess(surf, white, boardDotPos, self.ai)

	    if self.gameIsOver(boardDotPos, white):
	        return (False, self.ai)


	def move(self, surf, pos):

	    boardDot = (int(round(pos[0] / self.cellSize)), 
	    	int(round(pos[1] / self.cellSize)))

	    if boardDot[0] <= 0 or boardDot[0] > (self.numDivision - 1):
	        return
	    if boardDot[1] <= 0 or boardDot[1] > (self.numDivision - 1):
	        return

	    newPos = (boardDot[0] * self.cellSize, boardDot[1] * self.cellSize)
	    
	    if self.colorMatrix[boardDot[0]][boardDot[1]] is not None:
	        return None

	    currMove = (newPos, black)
	    self.addChess(surf, black, boardDot, self.user)

	    if self.gameIsOver(boardDot, black):
	        return (False, self.user)

	    return self.respond(surf, self.movements, currMove)







