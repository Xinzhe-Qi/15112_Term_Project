import pygame
import sys
from board import Board
from network import Network
from button import Button
from AI2 import *

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
grey            = (26, 26, 26)

pygame.init()
pygame.mixer.init()
win = pygame.display.set_mode((boardWidth, boardHeight))
pygame.display.set_caption("Five in Row")
clock = pygame.time.Clock()

hgImg = pygame.image.load("hg2.png")
hgImg = pygame.transform.scale(hgImg, (100, 100))
hgRect = hgImg.get_rect()
hgRect.center = (boardWidth / 2, boardHeight / 2 - 50)

# backgound Music
bgMusic = pygame.mixer.music.load('bgm.wav')
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(-1)

def drawBackground(win):
	bgImg = pygame.image.load("board.jpg").convert()
	background = pygame.transform.scale(bgImg, (boardWidth, boardHeight))
	bgRect = background.get_rect()

	win.blit(bgImg, bgRect)

	# draw board margins
	rectLines = [
			((cellSize, cellSize), (cellSize, boardHeight - cellSize)),
			((cellSize, cellSize), (boardWidth - cellSize, cellSize)),
			((cellSize, boardHeight - cellSize),(boardWidth - cellSize, boardHeight - cellSize)),
			((boardWidth - cellSize, cellSize), (boardWidth - cellSize, boardHeight - cellSize))
			]

	for line in rectLines:
			pygame.draw.line(win, black, line[0], line[1], 2)

	# draw board lines
	lineNum = numDivision - 2 - 1 # 16 - 2 - 1 = 13
	for i in range(lineNum):
		pygame.draw.line(win, black, (cellSize * (2 + i), cellSize),
										(cellSize * (2 + i), boardHeight - cellSize))
		pygame.draw.line(win, black, (cellSize, cellSize * (2 + i)),
										(boardHeight - cellSize, cellSize * (2 + i)))

	# draw points
	circleCenter = [
			(cellSize * 4, cellSize * 4),
			(boardWidth - cellSize * 4, cellSize * 4),
			(boardWidth - cellSize * 4, boardHeight - cellSize * 4),
			(cellSize * 4, boardHeight - cellSize * 4),
			(boardWidth // 2, boardHeight // 2)
			]

	for cc in circleCenter:
		pygame.draw.circle(win, black, cc, 5)


# draw the time limits
def drawTime(win, p1, p2):
	pygame.font.init()
	formatTime1 = str(int(p1//60)) + ":" + str(int(p1%60))
	formatTime2 = str(int(p2//60)) + ":" + str(int(p2%60))

	if int(p1%60) < 10:
		formatTime1 = formatTime1[:-1] + "0" + formatTime1[-1]
	if int(p2%60) < 10:
		formatTime2 = formatTime2[:-1] + "0" + formatTime2[-1]

	font = pygame.font.SysFont("SEASRN__.ttf", 30)
	txt = font.render("White Time: " + str(formatTime1), 1, white)
	txt2 = font.render("Black Time: " + str(formatTime2), 1, white)

	txt_rect = txt.get_rect()
	txt_rect.left = 0
	txt_rect.bottom = boardHeight

	txt2_rect = txt.get_rect()
	txt2_rect.right = boardWidth
	txt2_rect.bottom = boardHeight

	win.blit(txt, txt_rect)
	win.blit(txt2, txt2_rect)


# draw the instructions
def drawInstr(win, color, ready):
	font = pygame.font.Font("Amatic-Bold.ttf", 30)
	txt = font.render("Press q to Quit", 1, red)
	win.blit(txt, (10, 5))

	if not ready:
		bgImg = pygame.image.load("board.jpg").convert()
		background = pygame.transform.scale(bgImg, (boardWidth, boardHeight))
		bgRect = background.get_rect()
		win.blit(bgImg, bgRect)
		win.blit(hgImg, hgRect)
		
		font = pygame.font.Font("ChelaOne-Regular.ttf", 80)
		txt = font.render("Waiting for Player", 1, white)
		win.blit(txt, (boardWidth/2 - txt.get_width()/2, 300))

	if color == "s":
		txt3 = font.render("SPECTATOR MODE", 1, white)
		win.blit(txt3, (boardWidth/2-txt3.get_width()/2, 10))
	if color == "w":
		txt3 = font.render("YOU ARE WHITE", 1, white)
		win.blit(txt3, (boardWidth/2 - txt3.get_width()/2, 10))
	elif color == "b":
		txt3 = font.render("YOU ARE BLACK", 1, black)
		win.blit(txt3, (boardWidth/2 - txt3.get_width()/2, 10))

	if bo.turn == color:
		txt3 = font.render("YOUR TURN", 1, white)
		win.blit(txt3, (boardWidth/2 - txt3.get_width()/2, boardHeight - txt3.get_height()))
	else:
		txt3 = font.render("THEIR TURN", 1, white)
		win.blit(txt3, (boardWidth/2 - txt3.get_width()/2, boardHeight - txt3.get_height()))

def endScreen(win, text):
	s = pygame.Surface((boardWidth, boardHeight))
	s.set_alpha(128)
	s.fill(aquamarine3)
	win.blit(s, (0,0)) 

	font = pygame.font.Font("handlee-regular.ttf", 80)
	txt = font.render(text, 1, red)
	win.blit(txt, (boardWidth/2 - txt.get_width()/2, 300))
	pygame.display.update()

	pygame.time.set_timer(pygame.USEREVENT+1, 3000)

	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
				run = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					bo = n.send("reset")
					run = False
				elif event.type == pygame.USEREVENT+1:
					run = False

def redrawWin(win, bo, p1, p2, color, ready):
	drawBackground(win)
	bo.drawChess(win)
	drawTime(win, p1, p2)
	drawInstr(win, color, ready)

	pygame.display.update()

def connect():
	global n
	n = Network()
	return n.board

def main():
	global bo

	color = bo.start_user
	count = 0

	run = True

	while run:
		p1Time = bo.time1
		p2Time = bo.time2

		if count == 30:
			bo = n.send("get")
			count = 0
		else:
			count += 1
		clock.tick(30)

		redrawWin(win, bo, p1Time, p2Time, color, bo.ready)
		
		if p1Time <= 0:
			bo = n.send("winner b")
		elif p2Time <= 0:
			bo = n.send("winner w")

		if bo.isWinner("b"):
			bo = n.send("winner b")
		elif bo.isWinner("w"):
			bo = n.send("winner w")

		if bo.winner == "w":
			endScreen(win, "White is the Winner!")
			# run = False

		elif bo.winner == "b":
			endScreen(win, "Black is the winner")
			# run = False

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()

			elif event.type == pygame.MOUSEBUTTONDOWN and color != "s":
				if color == bo.turn and bo.ready:
					i, j = event.pos
					bo = n.send("move " + str(i) + " " + str(j) + " " + color)

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q and color != "s":
					if color == "w":
						bo = n.send("winner b")
					else:
						bo = n.send("winner w")

					pygame.time.wait(1000)
					run = False
				
	print("failed")
	n.disconnect()
	menuScreen(win)

def blit_text(surface, text, pos, font, color=pygame.Color('white')):
	words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
	space = font.size(' ')[0]  # The width of a space.
	max_width, max_height = surface.get_size()
	x, y = pos
	for line in words:
		for word in line:
			word_surface = font.render(word, 0, color)
			word_width, word_height = word_surface.get_size()
			if x + word_width >= max_width:
				x = pos[0]  # Reset the x.
				y += word_height  # Start on new row.
			surface.blit(word_surface, (x, y))
			x += word_width + space
		x = pos[0]  # Reset the x.
		y += word_height  # Start on new row.


def settingScreen(win):
	# Game Rule
	# Adjustments

	ruleButton = Button("Game Rule", boardWidth/2 - 100, boardHeight/3)
	adjustButton = Button("Adjust Game", boardWidth/2 - 100, boardHeight/3*2)
	returnButton = Button("Return", 0, 550)
	
	run = True
	while run:
		win.fill(black)

		ruleButton.draw(win)
		adjustButton.draw(win)
		returnButton.draw(win)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				run = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				if ruleButton.click(event.pos):
					ruleButton.clicked = True
					run = False
				elif adjustButton.click(event.pos):
					adjustButton.clicked = True
					run = False
				elif returnButton.click(event.pos):
					returnButton.clicked = True
					run = False
		pygame.display.update()

	if ruleButton.clicked == True:
		ruleScreen(win)
		# settingScreen(win)

	elif adjustButton.clicked == True:
		adjustScreen(win)

	elif returnButton.clicked == True:
		menuScreen(win)


def adjustScreen(win):
	returnButton = Button("Return", 0, 550)
	musicButton = Button("Music", 200, 400)
	boardSize = 15

	run = True
	while run:
		win.fill(black)
		font = pygame.font.Font("handlee-regular.ttf", 40)
		txt = font.render("Change Board Size: " + str(boardSize), True, white)
		win.blit(txt, (boardWidth/2 - txt.get_width()/2, 200))
		
		returnButton.draw(win)
		musicButton.draw(win)
		musicPaused = False
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				run = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if returnButton.click(event.pos):
					returnButton.clicked = True
					run = False
				elif musicButton.click(event.pos):
					pygame.mixer.music.pause()

			elif event.type == pygame.KEYDOWN:		
				if event.key == pygame.K_UP:
					boardSize += 1
				elif event.key == pygame.K_DOWN:
					boardSize -= 1
				elif event.key == pygame.K_r:
					boardSize = 15

		if returnButton.clicked == True:
			settingScreen(win)

		pygame.display.update()

def ruleScreen(win):

	returnButton = Button("Return", 0, 550)
	egImg = pygame.image.load("gomoku.gif")
	egImg = pygame.transform.scale(egImg, (300, 300))
	egRect = egImg.get_rect(topleft = (150, 350))

	run = True
	while run:
		win.fill(black)
		font = pygame.font.Font("handlee-regular.ttf", 40)
		text = "It is a board game for two players who take turns in putting black and white stones on the board. Each players' goal is to create an unbroken row of five stones horizontally, vertically, or diagonally."
 
		blit_text(win, text, (20, 20), font)

		returnButton.draw(win)

		win.blit(egImg, egRect)
	

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				run = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if returnButton.click(event.pos):
					returnButton.clicked = True
					settingScreen(win)
					run = False

		pygame.display.update()


def menuScreen(win):
	global bo
	run = True

	while run:
		# win.fill(white)
		bgImg = pygame.image.load("intro.jpg")
		background = pygame.transform.scale(bgImg, (boardWidth, boardHeight))
		bgRect = background.get_rect()
		win.blit(background, bgRect)

		font = pygame.font.Font("FFF_Tusj.ttf", 80)
		titleText = font.render("Gomoku", True, grey)
		win.blit(titleText, (boardWidth/2 - titleText.get_width()/2, 40 + boardHeight/2 - titleText.get_height()/2))
		
		spButton = Button("Single Player", 85, 500)
		mpButton = Button("Multi Player", 405, 500)

		setImg = pygame.image.load("setting.png")
		setting = pygame.transform.scale(setImg, (30, 30))
		setRect = setting.get_rect(topleft = (600, 10))
		setRectClicked = False
		win.blit(setting, setRect)


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
				run = False

			elif event.type == pygame.MOUSEBUTTONDOWN:
				if spButton.click(event.pos):
					spButton.clicked = True
					run = False
				elif mpButton.click(event.pos):
					mpButton.clicked = True
					run = False
				elif setRect.collidepoint(event.pos):
					setRectClicked = True
					run = False
					
			elif event.type == pygame.MOUSEMOTION:
				spButton.hover(event.pos)
				mpButton.hover(event.pos)

		spButton.draw(win)
		mpButton.draw(win)

		pygame.display.update()

	if mpButton.clicked:
		while True:
			try:
				bo = connect()
				print(bo)
				break
			except:
				print("Server Offline")
		main()
		menuScreen(win)
	elif spButton.clicked:
		runGame()
		menuScreen(win)
	elif setRectClicked:
		settingScreen(win)

menuScreen(win)



		


