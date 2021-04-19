import pygame
import time

fps = 30
boardWidth = 640
boardHeight = 640
numDivision = 16
numPoint = numDivision - 1
cellSize = boardWidth // numDivision
chessSize = boardWidth // 40

#                   R    G    B
white           = (255, 255, 255)
black           = (  0,   0,   0)
aquamarine3     = (102, 205, 170)
red             = (255,   0,   0)
blue            = (  0,   0, 255)

pygame.mixer.init()
hitSound = pygame.mixer.Sound('chess.wav')
hitSound.set_volume(0.1)

class Board:
    def __init__(self):
        self.board = [[None] * numPoint for i in range(numPoint)]
        self.color = None
        self.winner = False

        self.turn = "b"
        self.winner = ""

        self.ready = False

        self.time1 = 600
        self.time2 = 600

        self.storedTime1 = 0
        self.storedTime2 = 0

        self.startTime = time.time()

    def posToDotNum(self, pos):
        boardDotx, boardDoty = self.aroundToBoardDot(pos)
        dotNumx = int(boardDotx / cellSize - 1)
        dotNumy = int(boardDoty / cellSize - 1)
        return dotNumx, dotNumy

    def aroundToBoardDot(self, pos):
        return (int(round(pos[0] / cellSize)) * cellSize, 
                    int(round(pos[1] / cellSize)) * cellSize)

    def addMove(self, pos, color):
        changed = False

        i, j = self.posToDotNum(pos)
        boardDotx, boardDoty = self.aroundToBoardDot(pos)

        if color == "b":
            self.color = black
        elif color == "w":
            self.color = white

        if self.board[j][i] == None:
            hitSound.play()
            self.board[j][i] = ((boardDotx, boardDoty), self.color)
            changed = True

        if changed:
            if self.turn == "w":
                self.turn = "b"
            elif self.turn == "b":
                self.turn = "w"


    def drawChess(self, surf):
        for row in self.board:
            for col in row:
                if col == None:
                    pass
                else:
                    move, color = col
                    pygame.draw.circle(surf, color, move, chessSize)

    def isWinner(self, col):
        if col == "b":
            color = black
        elif col == "w":
            color = white

       # check horizontal spaces
        for x in range(numPoint - 4):
            for y in range(numPoint):
                if self.board[x][y] is not None and \
                    self.board[x+1][y] is not None and \
                    self.board[x+2][y] is not None and \
                    self.board[x+3][y] is not None and \
                    self.board[x+4][y] is not None:

                    if self.board[x][y][1] == color and \
                            self.board[x+1][y][1] == color and \
                            self.board[x+2][y][1] == color and \
                            self.board[x+3][y][1] == color and \
                            self.board[x+4][y][1] == color:
                        
                        self.winner = color
                        return True

                else:
                    pass

        # check vertical spaces
        for x in range(numPoint):
            for y in range(numPoint - 4):
                if self.board[x][y] is not None and \
                        self.board[x][y+1] is not None and \
                        self.board[x][y+2] is not None and \
                        self.board[x][y+3] is not None and \
                        self.board[x][y+4] is not None:
                    # print(x, y)

                    if self.board[x][y][1] == color and \
                            self.board[x][y+1][1] == color and \
                            self.board[x][y+2][1] == color and \
                            self.board[x][y+3][1] == color and \
                            self.board[x][y+4][1] == color:
                        
                        self.winner = color
                        return True
                else:
                    pass

        # check / diagonal spaces
        for x in range(numPoint - 4):
            for y in range(4, numPoint):
                if self.board[x][y] is not None and \
                    self.board[x+1][y-1] is not None and \
                    self.board[x+2][y-2] is not None and \
                    self.board[x+3][y-3] is not None and \
                    self.board[x+4][y-4] is not None:

                    if self.board[x][y][1] == color and \
                            self.board[x+1][y-1][1] == color and \
                            self.board[x+2][y-2][1] == color and \
                            self.board[x+3][y-3][1] == color and \
                            self.board[x+4][y-4][1] == color:
                        
                        self.winner = color
                        return True
                else:
                    pass

        # check \ diagonal spaces
        for x in range(numPoint - 4):
            for y in range(numPoint - 4):
                if self.board[x][y] is not None and \
                        self.board[x+1][y+1] is not None and \
                        self.board[x+2][y+2] is not None and \
                        self.board[x+3][y+3] is not None and \
                        self.board[x+4][y+4] is not None:

                    if self.board[x][y][1] == color and \
                            self.board[x+1][y+1][1] == color and \
                            self.board[x+2][y+2][1] == color and \
                            self.board[x+3][y+3][1] == color and \
                            self.board[x+4][y+4][1] == color:
                        
                        self.winner = color
                        return True

                else:
                    pass


